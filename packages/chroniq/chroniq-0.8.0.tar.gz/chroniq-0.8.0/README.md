# 🔮 Chroniq — Smart Versioning & Changelog CLI

![License](https://img.shields.io/github/license/BrandonAustin01/chroniq?style=flat-square)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square)
![Build](https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square)
![Made with ❤️](https://img.shields.io/badge/made%20with-%E2%9D%A4-red?style=flat-square)

**Chroniq** is your local-first, developer-friendly version manager + changelog tracker.  
It brings semantic versioning, rollback safety, and interactive changelog support — all from your terminal.

> _"Because versioning shouldn't feel like a chore."_ 💡

---

## 🚀 Features at a Glance

| 🧠 Feature                         | ✅ Support |
|-----------------------------------|------------|
| Semantic Versioning (SemVer)      | ✔️         |
| Pre-release Tags (alpha, beta)    | ✔️         |
| Interactive Changelog Prompts     | ✔️         |
| Rollback Support                  | ✔️         |
| Profile-based Config (.toml)      | ✔️         |
| Clean CLI Output (via rich)       | ✔️         |
| Zero Cloud Dependencies           | ✔️         |
| Full Test Coverage                | ✔️         |

---

## 🧰 Commands Overview

| Command                      | Purpose                                                   |
|------------------------------|-----------------------------------------------------------|
| `chroniq init`               | Initialize `version.txt` + `CHANGELOG.md`                 |
| `chroniq bump [level]`       | Bump version (`patch`, `minor`, `major`)                 |
| `chroniq bump --pre <tag>`   | Bump pre-release (`alpha`, `beta.1`, etc.)               |
| `chroniq rollback`           | Rollback latest version bump and changelog               |
| `chroniq log [--lines n]`    | Show last `n` changelog entries                          |
| `chroniq version`            | Display the current version                              |
| `chroniq reset`              | Delete version + changelog (use with caution)            |
| `chroniq audit [--strict]`   | Run diagnostic scan of config/version/changelog          |
| `chroniq config-show`        | Print merged active config, including profile             |
| `chroniq config set`         | Update config keys in `.chroniq.toml`                     |
| `chroniq changelog-preview`  | Preview formatted changelog block (dry-run entry)         |
| `chroniq test --smoke`       | Run smoke tests only                                      |
| `chroniq help`               | Show grouped help with style (coming 0.9.0)               |

---

## ✏️ Usage Examples

```bash
chroniq init                    # Sets up version.txt and CHANGELOG.md
chroniq bump minor              # Bumps 1.2.3 → 1.3.0
chroniq bump --pre rc           # Produces 1.3.0-rc.1
chroniq rollback                # Reverts to previous version and changelog
chroniq audit --strict          # Deep config/changelog validation
chroniq config set silent true  # Edit .chroniq.toml via CLI
```

---

## ⚙️ Config Options (`.chroniq.toml`)

Chroniq reads a config file (`.chroniq.toml`) with support for profiles and strict mode:

```toml
default_bump = "patch"
silent = false
strict = false
emoji_fallback = true
auto_increment_prerelease = true

[profile.dev]
default_bump = "minor"
silent = true

[profile.release]
strict = true
```

---

## 🧪 Test It

```bash
# Run all unittests
python -m unittest discover -s tests

# Or just smoke test the CLI
chroniq test --smoke
```

---

## 🧱 Project Structure

```
chroniq/
├── cli.py               # CLI entry point
├── core.py              # SemVer logic + rollback
├── config.py            # Config loading + updating
├── logger.py            # system_log + activity_log
├── changelog.py         # Add/preview entries
├── audit.py             # Diagnostic scanning
├── tests/               # Unit tests
├── version.txt          # Your current version
├── CHANGELOG.md         # Changelog entries
├── .chroniq.toml        # Config file (optional)
```

---

## 🤝 Contributing

PRs welcome — just follow:
- Keep it clean
- Keep it tested
- Keep it offline-safe

---

## 📄 License

[MIT](LICENSE) © Brandon McKinney
