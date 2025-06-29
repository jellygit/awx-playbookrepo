# HashiCorp Vault Ansible Plugins

[![ansible-test](https://github.com/flowerysong/ansible-flowerysong.hvault/actions/workflows/ansible-test.yml/badge.svg)](https://github.com/flowerysong/ansible-flowerysong.hvault/actions/workflows/ansible-test.yml)

This [Ansible](https://www.ansible.com/) collection implements
a number of plugins for interacting with [HashiCorp
Vault](https://vaultproject.io/). A complete set of low-level
operations (read, write, list, and delete) are available, so
functionality which does not yet have a higher-level interface should
still be possible to use. The implementation of high-level interfaces
prioritizes the subset of Vault functionality that I use.

## Dependencies

These plugins use standard Ansible features and require no extra
dependencies on the control node or target.

## Supported Ansible Versions

This collection is tested against the stable-2.16, stable-2.17,
stable-2.18, and devel branches of ansible-core. Other versions may or
may not work.

## Supported Vault Versions

This collection is tested against Vault 1.14. Other versions may or
may not work.

Some plugin interfaces include features specific to Vault Enterprise,
but no attempts are made to test that functionality.

## Where's the Documentation?

Documentation is not yet being built. If you have the collection
installed you can access each plugin's documentation via the
ansible-doc command, e.g. `ansible-doc flowerysong.hvault.engine` or
`ansible-doc -t lookup flowerysong.hvault.read`
