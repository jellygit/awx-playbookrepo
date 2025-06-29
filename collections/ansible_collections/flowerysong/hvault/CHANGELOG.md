# Changelog
All notable changes to this project will be documented in this file.

## 0.3.0 - 2024-12-10

### Added
- `ldap_config` - `username_as_alias` and `userfilter`
- `ssh_role` - `not_before_duration` and `default_extensions_template`
- `auth_aws` lookup.

### Changed
- retry after errors that might be transient
- improved error output

### Fixed
- plugin options now resolve templated values
- avoid `set_option()` errors on newer versions of ansible-core

## 0.2.0 - 2021-04-28

### Added
- `aws_auth_role` module.
- `aws_secret_role_iam` module.
- `aws_secret_role_sts` module.
- `ldap_config` module.
- `ldap_group` module.
- `ldap_user` module.

### Changed
- Added more information to the module return when an HTTP error causes the
  module to fail.
- Renamed the `url` parameter to `vault_addr`.

## 0.1.0 - 2021-04-21

Initial Release
