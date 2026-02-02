# Syncause JAVA SDK Uninstallation Guide

> [!IMPORTANT]
> Remove the SDK after debugging to restore original performance.

## Steps

1.  **Remove Profiles**: Delete the `disable-syncause-ai` and `auto-syncause-ai` profiles from `pom.xml`.
2.  **Remove Properties**: Delete the `syncause.repo.token.p1` and `syncause.repo.token.p2` properties from `pom.xml`.
3.  **Remove Repository**: Delete the `github-syncause` repository from `pom.xml`.
4.  **Remove Dependencies**: Delete `spring-boot-starter` and `bytebuddy-plugin` dependencies.
5.  **Remove Plugin**: Delete the `byte-buddy-maven-plugin` configuration from `<plugins>`.
6.  **Rebuild**: Run `mvn clean package` and restart the application.
