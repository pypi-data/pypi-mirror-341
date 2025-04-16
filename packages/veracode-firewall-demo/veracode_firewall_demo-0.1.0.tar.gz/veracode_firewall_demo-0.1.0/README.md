# Veracode Firewall Demo

This is an empty package which can be used for safely verifying that your
[package firewall] is blocking malicious packages.

This package does not contain any malicious code, but it is marked as malicious
in Veracode's [Threat Feed]. If your package firewall is configured correctly,
you will not be able to install this package. If your package firewall is
configured incorrectly, no malicious code is executed or downloaded when
installing this package.

[Threat Feed]: https://docs.phylum.io/knowledge_base/threat_feed

## Firewall Configuration

To setup Veracode's [package firewall] for your project, please follow the
[official documentation][setup].

[package firewall]: https://docs.phylum.io/package_firewall/about
[setup]: https://docs.phylum.io/package_firewall/about#configuration
