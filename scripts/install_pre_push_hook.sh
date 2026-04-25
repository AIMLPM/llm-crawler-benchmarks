#!/usr/bin/env bash
# Install a git pre-push hook that runs scripts/ci_local.sh before every
# push. Catches CI regressions locally so you don't get a flood of GitHub
# Actions failure emails.
#
# Usage:  scripts/install_pre_push_hook.sh
# Skip:   git push --no-verify   (one-off bypass)

set -e
cd "$(dirname "$0")/.."

HOOK=".git/hooks/pre-push"
mkdir -p .git/hooks

cat > "$HOOK" <<'EOF'
#!/usr/bin/env bash
# Auto-installed by scripts/install_pre_push_hook.sh
echo "[pre-push] running scripts/ci_local.sh ..."
if ! ./scripts/ci_local.sh; then
    echo "[pre-push] CI checks failed -- push aborted."
    echo "  fix the issues, or bypass once with: git push --no-verify"
    exit 1
fi
EOF

chmod +x "$HOOK"
echo "Installed $HOOK"
echo "Run 'git push' as usual; the hook will run ci_local.sh first."
echo "Bypass once: 'git push --no-verify'"
