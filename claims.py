import os
from typing import Any

import requests

DEFAULT_CLAIMS = ("repo", "repository_owner", "context", "actor_id", "actor")


def _parse_bool(value: str, env_name: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise ValueError(
        f"Invalid boolean value for {env_name}: {value!r}. "
        "Use one of: true/false, 1/0, yes/no, on/off."
    )


def _parse_claim_keys(value: str | None) -> list[str] | None:
    if value is None:
        return None
    items = [item.strip() for item in value.split(",")]
    filtered = [item for item in items if item]
    if not filtered:
        raise ValueError(
            "INCLUDE_CLAIM_KEYS is set but empty. "
            "Provide a comma-separated list, e.g. repo,repository_owner,actor."
        )
    return filtered


def _build_oidc_sub_customization_payload(
    use_default: bool, claims_keys: list[str] | None
) -> dict[str, Any]:
    payload: dict[str, Any] = {"use_default": use_default}
    if not use_default:
        payload["include_claim_keys"] = list(claims_keys or DEFAULT_CLAIMS)
    return payload


def claims(
    github_token: str,
    use_default: bool = False,
    claims_keys: list[str] | None = None,
    organisation: str = "wlodarczyk-devops",
    repository: str = "shared-modules",
    github_api: str = "https://api.github.com",
) -> dict[str, Any]:
    oidc_sub_customization_payload = _build_oidc_sub_customization_payload(
        use_default=use_default,
        claims_keys=claims_keys,
    )

    request_headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    url = f"{github_api}/repos/{organisation}/{repository}/actions/oidc/customization/sub"
    request_api = requests.put(
        url,
        headers=request_headers,
        json=oidc_sub_customization_payload,
        timeout=30,
    )
    request_api.raise_for_status()
    return request_api.json()


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def main() -> int:
    try:
        github_token = _required_env("GITHUB_TOKEN")
        organisation = _required_env("ORGANISATION")
        repository = _required_env("REPOSITORY")
        github_api = os.getenv("GITHUB_API", "https://api.github.com")
        use_default = _parse_bool(os.getenv("USE_DEFAULT", "false"), "USE_DEFAULT")
        claims_keys = _parse_claim_keys(os.getenv("INCLUDE_CLAIM_KEYS"))

        response = claims(
            github_token=github_token,
            use_default=use_default,
            claims_keys=claims_keys,
            organisation=organisation,
            repository=repository,
            github_api=github_api,
        )
        print(
            f"Claims updated for {organisation}/{repository}. "
            f"use_default={use_default}; "
            f"claim_keys={claims_keys or list(DEFAULT_CLAIMS)}"
        )
        return 0
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        return 1
    except requests.RequestException as exc:
        print(f"GitHub API error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
