#!/usr/bin/env python3
"""
workstation-setup.py — provision an office/paperwork toolchain on Ubuntu 24.04 LTS.

Idempotent: it CHECKS what is already present, installs ONLY what is missing, then
applies light configuration (printer/scanner services, spell language, browser
default). It installs a lean office/paperwork set only — no dev/ML/database stack.
The Arad Smart Meters / Wine / NFC side is handled separately by SETUP-GUIDE.md.

USAGE
    python3 workstation-setup.py --check                    # dry run: report only
    sudo python3 workstation-setup.py                       # install missing + configure
    sudo python3 workstation-setup.py --only office,pdf,print   # just those categories
    sudo python3 workstation-setup.py --list               # list categories and exit
"""

import argparse
import os
import shutil
import subprocess
import sys

# ---------------------------------------------------------------------------
# WHAT TO INSTALL — grouped by category. Mirrors the work/paperwork subset of
# the main machine. Each entry: how to detect it + how to install it.
# ---------------------------------------------------------------------------

# Standard apt packages (present in Ubuntu's own repos — always safe).
APT = {
    "office":  ["libreoffice", "libreoffice-draw"],
    "spell":   ["hunspell-en-gb", "hunspell-en-au", "hunspell-en-ca",
                "hunspell-en-za", "wbritish"],
    "pdf":     ["qpdf", "img2pdf", "imagemagick", "libimage-exiftool-perl"],
    "print":   ["cups", "simple-scan", "sane-utils", "avahi-daemon", "avahi-utils"],
    "files":   ["filezilla"],
    "utils":   ["htop", "curl", "git", "gnupg", "net-tools", "tmux"],
}

# Snap apps (work subset). firefox + thunderbird ship by default on 24.04 desktop;
# we check and only add if somehow missing.
SNAPS = {
    "browsers": ["chromium", "firefox"],
    "office":   ["onlyoffice-desktopeditors"],
    "mail":     ["thunderbird"],
    "image":    ["pinta"],
}

# Third-party apt repos we set up ourselves, then install from.
#   key_url  : the signing key (dearmored into /usr/share/keyrings)
#   list     : the sources.list.d line (with [signed-by=...] placeholder {KEY})
#   packages : what to install once the repo is live
THIRD_PARTY_REPOS = {
    "chrome": {
        "category": "browsers",
        "keyring": "/usr/share/keyrings/google-chrome.gpg",
        "key_url": "https://dl.google.com/linux/linux_signing_key.pub",
        "list_path": "/etc/apt/sources.list.d/google-chrome.list",
        "list_line": "deb [arch=amd64 signed-by={KEY}] "
                     "http://dl.google.com/linux/chrome/deb/ stable main",
        "packages": ["google-chrome-stable"],
    },
    "protonvpn": {
        # Proton publishes a 'release' .deb that wires up their apt repo, then
        # proton-vpn-gnome-desktop installs from it.
        "category": "proton",
        "release_deb": "https://repo.protonvpn.com/debian/dists/stable/main/"
                       "binary-all/protonvpn-stable-release_1.0.8_all.deb",
        "packages": ["proton-vpn-gnome-desktop"],
    },
}

# Version-fragile direct .deb downloads. We ATTEMPT the known URL; if it 404s or
# the URL has moved, we DO NOT fail silently — we print a clear MANUAL step with
# the official download page so nothing is quietly skipped.
DIRECT_DEBS = {
    "protonmail": {
        "category": "proton",
        "detect": "proton-mail",           # dpkg package name
        "url": "https://proton.me/download/mail/linux/ProtonMail-desktop.deb",
        "manual": "https://proton.me/mail/download",
    },
    "protonbridge": {
        "category": "proton",
        "detect": "protonmail-bridge",
        "url": "https://proton.me/download/bridge/protonmail-bridge_3.16.0-1_amd64.deb",
        "manual": "https://proton.me/mail/bridge",
    },
    "obsidian": {
        "category": "notes",
        "detect": "obsidian",
        # Resolved dynamically from GitHub's latest release (see resolve_obsidian).
        "url": None,
        "manual": "https://obsidian.md/download",
    },
}

CONFIG_DEB_SIZE_MIN = 50_000   # a real .deb is bigger than this; guards against HTML error pages

# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

class C:
    G = "\033[92m"; Y = "\033[93m"; R = "\033[91m"; B = "\033[94m"; DIM = "\033[2m"; X = "\033[0m"

results = {"installed": [], "already": [], "failed": [], "manual": []}


def say(msg, colour=""):
    print(f"{colour}{msg}{C.X}" if colour else msg, flush=True)


def run(cmd, check=True, capture=False):
    """Run a shell command (list form). Returns CompletedProcess."""
    return subprocess.run(cmd, check=check,
                          stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.STDOUT if capture else None,
                          text=True)


def apt_installed(pkg):
    r = subprocess.run(["dpkg-query", "-W", "-f=${Status}", pkg],
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    return "install ok installed" in r.stdout


def snap_installed(name):
    r = subprocess.run(["snap", "list", name],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return r.returncode == 0


def have_cmd(name):
    return shutil.which(name) is not None


# ---------------------------------------------------------------------------
# Installers
# ---------------------------------------------------------------------------

def apt_update():
    if DRY:
        say("  would run: apt-get update", C.DIM); return
    run(["apt-get", "update", "-qq"], check=False)


def install_apt(pkgs, label):
    missing = [p for p in pkgs if not apt_installed(p)]
    for p in pkgs:
        if p not in missing:
            results["already"].append(p)
    if not missing:
        say(f"  [{label}] all present", C.DIM); return
    say(f"  [{label}] installing: {', '.join(missing)}", C.B)
    if DRY:
        return
    r = run(["apt-get", "install", "-y", "--no-install-recommends", *missing], check=False)
    for p in missing:
        (results["installed"] if apt_installed(p) else results["failed"]).append(p)


def install_snap(name):
    if snap_installed(name):
        results["already"].append(f"snap:{name}"); say(f"  [snap] {name} present", C.DIM); return
    say(f"  [snap] installing {name}", C.B)
    if DRY:
        return
    r = run(["snap", "install", name], check=False)
    (results["installed"] if snap_installed(name) else results["failed"]).append(f"snap:{name}")


def setup_chrome_repo(spec):
    if apt_installed("google-chrome-stable"):
        results["already"].append("google-chrome-stable"); say("  [chrome] present", C.DIM); return
    say("  [chrome] adding Google apt repo + key", C.B)
    if DRY:
        return
    try:
        key = run(["curl", "-fsSL", spec["key_url"]], capture=True).stdout
        p = subprocess.run(["gpg", "--dearmor", "-o", spec["keyring"]],
                           input=key.encode() if isinstance(key, str) else key, check=True)
        with open(spec["list_path"], "w") as f:
            f.write(spec["list_line"].replace("{KEY}", spec["keyring"]) + "\n")
        apt_update()
        run(["apt-get", "install", "-y", "google-chrome-stable"], check=False)
    except Exception as e:
        say(f"  [chrome] repo setup failed: {e}", C.R)
    (results["installed"] if apt_installed("google-chrome-stable")
     else results["failed"]).append("google-chrome-stable")


def setup_protonvpn(spec):
    if apt_installed("proton-vpn-gnome-desktop"):
        results["already"].append("proton-vpn-gnome-desktop"); say("  [protonvpn] present", C.DIM); return
    say("  [protonvpn] adding Proton repo (release deb) + installing", C.B)
    if DRY:
        return
    tmp = "/tmp/protonvpn-release.deb"
    ok = download(spec["release_deb"], tmp)
    if ok:
        run(["apt-get", "install", "-y", tmp], check=False)
        apt_update()
        run(["apt-get", "install", "-y", "proton-vpn-gnome-desktop"], check=False)
    (results["installed"] if apt_installed("proton-vpn-gnome-desktop")
     else results["failed"]).append("proton-vpn-gnome-desktop")


def download(url, dest):
    """Download to dest. Returns True only if we got a plausibly-real file."""
    r = subprocess.run(["curl", "-fsSL", "-o", dest, url], check=False)
    if r.returncode != 0 or not os.path.exists(dest):
        return False
    if os.path.getsize(dest) < CONFIG_DEB_SIZE_MIN:
        os.remove(dest); return False
    return True


def resolve_obsidian(spec):
    """Find the latest Obsidian amd64 .deb URL from GitHub releases."""
    try:
        import json, urllib.request
        api = "https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest"
        with urllib.request.urlopen(api, timeout=15) as resp:
            data = json.load(resp)
        for asset in data.get("assets", []):
            n = asset["name"]
            if n.endswith("_amd64.deb") or (n.endswith(".deb") and "arm" not in n):
                return asset["browser_download_url"]
    except Exception:
        pass
    return None


def install_direct_deb(name, spec):
    if apt_installed(spec["detect"]):
        results["already"].append(spec["detect"]); say(f"  [{name}] present", C.DIM); return
    url = spec["url"] or (resolve_obsidian(spec) if name == "obsidian" else None)
    say(f"  [{name}] installing", C.B)
    if DRY:
        if not url:
            say(f"  [{name}] (would resolve download URL at run time)", C.DIM)
        return
    tmp = f"/tmp/{name}.deb"
    if url and download(url, tmp):
        run(["apt-get", "install", "-y", tmp], check=False)
    if apt_installed(spec["detect"]):
        results["installed"].append(spec["detect"])
    else:
        results["manual"].append((spec["detect"], spec["manual"]))
        say(f"  [{name}] auto-install unavailable → MANUAL: {spec['manual']}", C.Y)


# ---------------------------------------------------------------------------
# Configuration (light, safe, idempotent)
# ---------------------------------------------------------------------------

def configure():
    say("\n== Configuration ==", C.B)
    # Printer + scanner discovery services
    for svc in ("cups", "avahi-daemon"):
        if DRY:
            say(f"  would enable service: {svc}", C.DIM); continue
        run(["systemctl", "enable", "--now", svc], check=False)
        say(f"  service enabled: {svc}", C.G)
    # Add the real user to lpadmin so they can manage printers without root
    user = os.environ.get("SUDO_USER")
    if user:
        if DRY:
            say(f"  would add {user} to lpadmin group", C.DIM)
        else:
            run(["usermod", "-aG", "lpadmin", user], check=False)
            say(f"  {user} added to lpadmin group", C.G)
    # Default spell/UI language is en-GB via the hunspell-en-gb package (installed above);
    # LibreOffice picks it up automatically. Nothing else to force.
    say("  spell dictionary en-GB in place (LibreOffice uses it automatically)", C.DIM)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def all_categories():
    cats = set()
    for group in (APT, SNAPS):
        cats.update(group.keys())
    for spec in list(THIRD_PARTY_REPOS.values()) + list(DIRECT_DEBS.values()):
        cats.add(spec["category"])
    return sorted(cats)


def main():
    global DRY
    ap = argparse.ArgumentParser(description="Set up an office/paperwork toolchain on Ubuntu.")
    ap.add_argument("--check", action="store_true", help="dry run — report only, change nothing")
    ap.add_argument("--only", help="comma-separated categories (see --list)")
    ap.add_argument("--list", action="store_true", help="list categories and exit")
    args = ap.parse_args()

    if args.list:
        say("Categories: " + ", ".join(all_categories()))
        say("Default: install everything missing across all categories.")
        return

    DRY = args.check
    only = set(args.only.split(",")) if args.only else None

    if not DRY and os.geteuid() != 0:
        say("This needs root to install. Re-run with:  sudo python3 workstation-setup.py", C.R)
        sys.exit(1)

    say(f"{C.B}=== workstation setup {'(DRY RUN)' if DRY else ''} ==={C.X}")
    say(f"{C.DIM}Ubuntu target · idempotent · installs only what's missing{C.X}\n")

    if not DRY:
        apt_update()

    def want(cat):
        return only is None or cat in only

    say("== APT (standard Ubuntu repos) ==", C.B)
    for cat, pkgs in APT.items():
        if want(cat):
            install_apt(pkgs, cat)

    say("\n== Snap apps ==", C.B)
    for cat, names in SNAPS.items():
        if want(cat):
            for n in names:
                install_snap(n)

    say("\n== Third-party repos ==", C.B)
    if want("browsers"):
        setup_chrome_repo(THIRD_PARTY_REPOS["chrome"])
    if want("proton"):
        setup_protonvpn(THIRD_PARTY_REPOS["protonvpn"])

    say("\n== Proton Mail / Bridge / Obsidian ==", C.B)
    for name, spec in DIRECT_DEBS.items():
        if want(spec["category"]):
            install_direct_deb(name, spec)

    configure()

    # ---- Summary ----
    say(f"\n{C.B}=== Summary ==={C.X}")
    say(f"  {C.G}Installed now : {len(results['installed'])}{C.X}  {', '.join(results['installed']) or '-'}")
    say(f"  {C.DIM}Already present: {len(results['already'])}{C.X}")
    if results["failed"]:
        say(f"  {C.R}Failed        : {len(results['failed'])}  {', '.join(results['failed'])}{C.X}")
    if results["manual"]:
        say(f"  {C.Y}Manual needed :{C.X}")
        for pkg, url in results["manual"]:
            say(f"      - {pkg}: {url}", C.Y)
    if DRY:
        say(f"\n{C.Y}Dry run — nothing was changed. Re-run with sudo to apply.{C.X}")
    else:
        say(f"\n{C.G}Done. Log out/in once so the lpadmin group + snap PATH take effect.{C.X}")
        say(f"{C.DIM}Next: Proton Mail/Bridge need an interactive login. Arad meters → see SETUP-GUIDE.md.{C.X}")


if __name__ == "__main__":
    DRY = False
    main()
