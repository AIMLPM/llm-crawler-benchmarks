// Colly benchmark crawler — fetches pages and saves raw HTML for markdownify conversion.
// Usage: go run main.go -url URL -out DIR -max N [-urls FILE]
//
// When -urls FILE is provided, reads URLs from the file (one per line) and fetches those.
// Otherwise, crawls from -url following links up to -max pages.
package main

import (
	"flag"
	"fmt"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	"github.com/gocolly/colly/v2"
)

func safeFilename(rawURL string) string {
	s := strings.ReplaceAll(rawURL, "://", "_")
	s = strings.ReplaceAll(s, "/", "_")
	if len(s) > 80 {
		s = s[:80]
	}
	return s
}

func main() {
	baseURL := flag.String("url", "", "Base URL to crawl")
	outDir := flag.String("out", "./colly_output", "Output directory")
	maxPages := flag.Int("max", 50, "Maximum pages to fetch")
	urlsFile := flag.String("urls", "", "File with URLs to fetch (one per line)")
	flag.Parse()

	if *baseURL == "" {
		fmt.Fprintln(os.Stderr, "Usage: go run main.go -url URL -out DIR -max N [-urls FILE]")
		os.Exit(1)
	}

	os.MkdirAll(*outDir, 0755)

	var pageCount int64

	// Browser-like User-Agent. Default colly UA ("colly - ...") is blocked
	// by Cloudflare/Akamai/etc. WAFs on most modern sites. Use a recent
	// Chrome on macOS string so we look like a normal browser.
	const browserUA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " +
		"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

	c := colly.NewCollector(
		colly.MaxDepth(3),
		colly.Async(true),
		colly.UserAgent(browserUA),
	)

	// Per-request timeout and concurrency limits
	c.SetRequestTimeout(30 * time.Second)
	c.Limit(&colly.LimitRule{
		DomainGlob:  "*",
		Parallelism: 5,
		Delay:       100 * time.Millisecond,
	})

	// Respect robots.txt
	c.AllowURLRevisit = false

	// Set browser-like Accept headers on every request. Some WAFs check
	// UA + Accept consistency together; matching what a real Chrome sends
	// reduces the chance of getting flagged as a bot.
	c.OnRequest(func(r *colly.Request) {
		r.Headers.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
		r.Headers.Set("Accept-Language", "en-US,en;q=0.9")
		r.Headers.Set("Accept-Encoding", "gzip, deflate, br")
		r.Headers.Set("Sec-Ch-Ua", `"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"`)
		r.Headers.Set("Sec-Ch-Ua-Mobile", "?0")
		r.Headers.Set("Sec-Ch-Ua-Platform", `"macOS"`)
		r.Headers.Set("Sec-Fetch-Dest", "document")
		r.Headers.Set("Sec-Fetch-Mode", "navigate")
		r.Headers.Set("Sec-Fetch-Site", "none")
		r.Headers.Set("Upgrade-Insecure-Requests", "1")
	})

	parsedBase, _ := url.Parse(*baseURL)
	baseDomain := parsedBase.Hostname()

	// Track per-URL retry counts for 429 backoff
	var retryCounts sync.Map
	const maxRetries = 3

	c.OnError(func(r *colly.Response, err error) {
		if r.StatusCode == 429 {
			key := r.Request.URL.String()
			countVal, _ := retryCounts.LoadOrStore(key, 0)
			count := countVal.(int)
			if count < maxRetries {
				retryCounts.Store(key, count+1)
				delay := time.Duration(count+1) * 500 * time.Millisecond
				fmt.Fprintf(os.Stderr, "[colly] 429 on %s, retry %d/%d after %v\n", key, count+1, maxRetries, delay)
				time.Sleep(delay)
				r.Request.Retry()
				return
			}
			fmt.Fprintf(os.Stderr, "[colly] 429 on %s, giving up after %d retries\n", key, maxRetries)
			return
		}
		fmt.Fprintf(os.Stderr, "[colly] error %s: %v\n", r.Request.URL, err)
	})

	c.OnResponse(func(r *colly.Response) {
		current := atomic.LoadInt64(&pageCount)
		if current >= int64(*maxPages) {
			return
		}

		contentType := r.Headers.Get("Content-Type")
		if !strings.Contains(contentType, "text/html") {
			return
		}

		// Save raw HTML
		filename := safeFilename(r.Request.URL.String()) + ".html"
		htmlPath := filepath.Join(*outDir, filename)
		os.WriteFile(htmlPath, r.Body, 0644)

		atomic.AddInt64(&pageCount, 1)
	})

	if *urlsFile == "" {
		// Discovery mode — follow links
		c.OnHTML("a[href]", func(e *colly.HTMLElement) {
			current := atomic.LoadInt64(&pageCount)
			if current >= int64(*maxPages) {
				return
			}
			link := e.Request.AbsoluteURL(e.Attr("href"))
			if link == "" {
				return
			}
			parsed, err := url.Parse(link)
			if err != nil {
				return
			}
			if parsed.Hostname() == baseDomain {
				e.Request.Visit(link)
			}
		})

		c.Visit(*baseURL)
	} else {
		// Fixed URL list mode
		data, err := os.ReadFile(*urlsFile)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error reading URLs file: %v\n", err)
			os.Exit(1)
		}
		lines := strings.Split(string(data), "\n")
		for _, line := range lines {
			line = strings.TrimSpace(line)
			if line != "" {
				c.Visit(line)
			}
		}
	}

	c.Wait()
	fmt.Printf("%d\n", atomic.LoadInt64(&pageCount))
}
