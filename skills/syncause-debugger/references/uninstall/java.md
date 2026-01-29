# Syncause JAVA SDK Uninstallation Guide

> [!IMPORTANT]
> Remove the SDK after debugging to restore original performance.

## Steps

1.  **Remove Profiles**: Delete the `disable-syncause-ai` and `auto-syncause-ai` profiles from `pom.xml`.
2.  **Remove Repository**: Delete the `github-syncause` repository from `pom.xml`.
3.  **Remove Dependencies**: Delete `spring-boot-starter` and `bytebuddy-plugin` dependencies.
4.  **Remove Plugin**: Delete the `byte-buddy-maven-plugin` configuration from `<plugins>`.
5.  **Rebuild**: Run `mvn clean package` and restart the application.
