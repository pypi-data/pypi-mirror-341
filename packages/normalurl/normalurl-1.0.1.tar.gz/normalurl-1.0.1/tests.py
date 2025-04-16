from typing import Generator

from normalurl import _urlparse as urlparse, normalize_url

urls = [
	"localhost",
	"127.0.0.1",
	"example.org",
	"sub.domain.com",
	"localhost:12345",
	"127.0.0.1:12345",
	"example.org:12345",
	"sub.domain.com:12345",
	"localhost/",
	"127.0.0.1/",
	"example.org/",
	"sub.domain.com/",
	"localhost:12345/",
	"127.0.0.1:12345/",
	"example.org:12345/",
	"sub.domain.com:12345/",
	"localhost/get/a?x=1&y=2%203",
	"127.0.0.1/get/a?x=1&y=2%203",
	"example.org/get/a?x=1&y=2%203",
	"sub.domain.com/get/a?x=1&y=2%203",
	"localhost:12345/get/a?x=1&y=2%203",
	"127.0.0.1:12345/get/a?x=1&y=2%203",
	"example.org:12345/get/a?x=1&y=2%203",
	"sub.domain.com:12345/get/a?x=1&y=2%203",
	"http://localhost",
	"http://127.0.0.1",
	"http://example.org",
	"http://sub.domain.com",
	"http://localhost:12345",
	"http://127.0.0.1:12345",
	"http://example.org:12345",
	"http://sub.domain.com:12345",
	"http://localhost/",
	"http://127.0.0.1/",
	"http://example.org/",
	"http://sub.domain.com/",
	"http://localhost:12345/",
	"http://127.0.0.1:12345/",
	"http://example.org:12345/",
	"http://sub.domain.com:12345/",
	"http://localhost/get/a?x=1&y=2%203",
	"http://127.0.0.1/get/a?x=1&y=2%203",
	"http://example.org/get/a?x=1&y=2%203",
	"http://sub.domain.com/get/a?x=1&y=2%203",
	"http://localhost:12345/get/a?x=1&y=2%203",
	"http://127.0.0.1:12345/get/a?x=1&y=2%203",
	"http://example.org:12345/get/a?x=1&y=2%203",
	"http://sub.domain.com:12345/get/a?x=1&y=2%203#11",
]


def _get_all_url_variants(
		scheme: str,
		hostname: str,
		port: str,
		path: str,
		query: str,
		fragment: str,
		username: str,
		password: str,
) -> Generator[str, None, None]:
	if path.startswith("/"):
		path = path[1:]
	if path.endswith("/"):
		path = path[:-1]
	for s in [f"{scheme}://", "//", ""]:
		for h in [hostname, ""]:
			for p in [f":{port}", ""]:
				for t in [f"/{path}", f"/{path}", ""]:
					for q in [f"?{query}", ""]:
						for f in [f"#{fragment}", ""]:
							for auth in [f"{username}:{password}@", f"{username}@", ""]:
								yield f"{s}{auth}{h}{p}{t}{q}{f}"


def _build_url(
		scheme: str,
		hostname: str,
		port: str,
		path: str,
		query: str,
		fragment: str,
		username: str,
		password: str,
) -> str:
	return (
		f"{scheme}://{username}:{password}@{hostname}:{port}{path}?{query}#{fragment}"
	)


def _assert_norm(url, norm, condition=lambda u, n: u == n):
	print(url, "→", norm)
	assert condition(url, norm), url


def test_native():
	for url in urls:
		_assert_norm(url, urlparse(url).geturl())


def test_normalize_url():
	for url in urls:
		_assert_norm(url, normalize_url(url))


def test_normalize_url_scheme():
	for url in urls:
		_assert_norm(
				url,
				normalize_url(url, scheme="http"),
				lambda u, n: n.startswith("http://") and u in n,
		)


def test_normalize_url_port():
	for url in urls:
		_assert_norm(
				url,
				normalize_url(url, port="1122"),
				lambda u, n: (":1122" in n or ":12345" in n)
							 and u == n.replace(":1122", ""),
		)


def test_normalize_url_scheme_port():
	for url in urls:
		_assert_norm(
				url,
				normalize_url(url, scheme="http", port="1122"),
				lambda u, n: n.startswith("http://") and (":1122" in n or ":12345" in n),
		)


def test_auth():
	url_descriptor = {
		"scheme"  : "http",
		"hostname": "example.org",
		"port"    : "12345",
		"path"    : "/get/page",
		"query"   : "x=1&y=2%203",
		"fragment": "toc",
		"username": "admin",
		"password": "pass",
	}
	correct_url = _build_url(**url_descriptor)
	for url in _get_all_url_variants(**url_descriptor):
		normalized_url = normalize_url(url, **url_descriptor)
		assert normalized_url == correct_url, normalized_url
