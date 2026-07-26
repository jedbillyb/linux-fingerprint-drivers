#!/bin/sh
# detect.sh - find your fingerprint sensor and report what this repo knows about
# it. With no arguments it scans USB; you can also pass IDs directly:
#
#   ./tools/detect.sh
#   ./tools/detect.sh 27c6:55b4 04f3:0c4c
#
# POSIX sh; needs lsusb (usbutils) for the scan.

set -eu

repo=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
devices="$repo/devices"
readme="$repo/README.md"
unsupported="$repo/docs/unsupported-devices.md"

# Vendor IDs known to ship fingerprint sensors, per the libfprint wiki.
fp_vendors="047d 04e8 04f3 05ba 06cb 0a5c 0bda 10a5 1188 138a 147e 1491 16d1
1c7a 2541 27c6 2808 298d 2df0 3274 3538"

is_fp_vendor() {
	for v in $fp_vendors; do
		[ "$1" = "$v" ] && return 0
	done
	return 1
}

# report <vendor:product> [description]
report() {
	id=$1
	desc=${2:-}

	printf '\n=== %s %s\n' "$id" "$desc"

	if [ -d "$devices/$id" ]; then
		printf 'Entry in this repo: devices/%s/\n' "$id"
		sed -n 's/^\*\*Status: *\([^*]*\)\*\*.*/Status: \1/p' \
			"$devices/$id/README.md" | head -1
		grep -F "$id" "$readme" | grep -F '|' | head -3 |
			sed 's/^/  README: /'
		printf 'Read devices/%s/README.md, then docs/BUILD.md for build steps.\n' "$id"
		return
	fi

	# Many entries cover several product IDs (one driver, a family of sensors),
	# so an ID with no directory of its own may still be documented inside one.
	owner=$(grep -lF "$id" "$devices"/*/README.md 2>/dev/null | head -1)
	if [ -n "$owner" ]; then
		entry=$(basename "$(dirname "$owner")")
		printf 'Covered by entry devices/%s/ (that entry handles several product IDs).\n' \
			"$entry"
		sed -n 's/^\*\*Status: *\([^*]*\)\*\*.*/Status: \1/p' "$owner" | head -1
		printf 'Read devices/%s/README.md, then docs/BUILD.md for build steps.\n' "$entry"
		return
	fi

	if grep -qF "$id" "$readme" 2>/dev/null; then
		printf 'Mentioned in README.md - check the surrounding table:\n'
		grep -nF "$id" "$readme" | head -3 | sed 's/^/  /'
		return
	fi

	if [ -f "$unsupported" ] && grep -qF "$id" "$unsupported"; then
		printf 'Known UNSUPPORTED: on the libfprint wiki list, no driver here or upstream.\n'
		grep -F "$id" "$unsupported" | head -1 | sed 's/^/  /'
		printf 'If you get it working, a contribution is very welcome - see CONTRIBUTING.md\n'
		return
	fi

	cat <<-EOF
	Not known to this repo or to the libfprint unsupported-devices list.
	Check whether upstream libfprint already supports it:
	  https://fprint.freedesktop.org/supported-devices.html
	EOF
}

if [ $# -gt 0 ]; then
	for arg; do
		report "$(printf '%s' "$arg" | tr '[:upper:]' '[:lower:]')"
	done
	exit 0
fi

if ! command -v lsusb >/dev/null 2>&1; then
	echo "lsusb not found - install usbutils, or pass an ID: $0 27c6:55b4" >&2
	exit 1
fi

echo "Scanning USB for likely fingerprint sensors..."

matches=$(mktemp)
trap 'rm -f "$matches"' EXIT HUP INT TERM

# lsusb line: "Bus 003 Device 002: ID 27c6:55b4 Vendor Product"
lsusb | while IFS= read -r line; do
	id=$(printf '%s' "$line" | sed -n 's/^Bus .* ID \([0-9a-fA-F]\{4\}:[0-9a-fA-F]\{4\}\).*/\1/p')
	[ -n "$id" ] || continue
	desc=${line#*"$id"}
	case $desc in
	*[Ff]inger* | *[Ff]print* | *iometric* | *[Vv]alidity* | *[Gg]oodix*)
		printf '%s\t%s\n' "$id" "$desc" >>"$matches"
		continue
		;;
	esac
	if is_fp_vendor "$(printf '%s' "${id%%:*}" | tr '[:upper:]' '[:lower:]')"; then
		printf '%s\t%s (matched on vendor ID - may not be the reader)\n' \
			"$id" "$desc" >>"$matches"
	fi
done

if [ -s "$matches" ]; then
	while IFS="$(printf '\t')" read -r id desc; do
		report "$(printf '%s' "$id" | tr '[:upper:]' '[:lower:]')" "$desc"
	done <"$matches"
else
	cat <<-'EOF'

	No likely fingerprint sensor found on USB.

	Many newer sensors are not on USB at all - they hang off SPI or I2C and will
	never appear in lsusb. Check:
	  ls /sys/bus/spi/devices/
	  sudo dmesg | grep -iE 'fingerprint|fpc|elan|goodix|synaptic'
	and the wiki's SPI Devices section:
	  https://gitlab.freedesktop.org/libfprint/wiki/-/wikis/Unsupported-Devices
	EOF
fi
