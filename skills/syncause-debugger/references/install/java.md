# Syncause JAVA SDK Installation Guide

> **Note:** For all steps below, if the corresponding section (e.g., `<properties>`, `<dependencies>`) already exists in your `pom.xml`, simply add the new tags inside the existing section.

## Step 1: Add Profiles
Add these profiles to manage the SDK's activation state:

```xml
    <profiles>
        <profile>
            <id>disable-syncause-ai</id>
            <properties>
                <syncause.disable>true</syncause.disable>
            </properties>
        </profile>
        <profile>
            <id>auto-syncause-ai</id>
            <properties>
                <syncause.disable.profiles>prod</syncause.disable.profiles>
            </properties>
        </profile>
    </profiles>
```

## Step 2: Configure Repository & Token
Add these properties and the repository to your `pom.xml`.

```xml
    <properties>
        <syncause.repo.token.p1>github_pat_11B3DNTTY0J3sz8C2CQUuT_fDRzzDxHDeWYrwgAGDzzD</syncause.repo.token.p1>
        <syncause.repo.token.p2>7rsIhveWt8Y4wEORjxqkIiD6W2A2CWqovpdcE0</syncause.repo.token.p2>
    </properties>

    <repositories>
        <repository>
            <id>github-syncause</id>
            <name>GitHub Packages</name>
            <url>https://syn-cause:${syncause.repo.token.p1}${syncause.repo.token.p2}@maven.pkg.github.com/Syncause/syncause-sdk</url>
        </repository>
    </repositories>
```

## Step 3: Add Dependencies
Add the following dependencies:

```xml
        <dependency>
            <groupId>com.syncause</groupId>
            <artifactId>spring-boot-starter</artifactId>
            <version>0.2.7</version>
        </dependency>
        <dependency>
            <groupId>com.syncause</groupId>
            <artifactId>bytebuddy-plugin</artifactId>
            <version>0.2.7</version>
        </dependency>
```

## Step 4: Configure Plugin
Add the `byte-buddy-maven-plugin` to your `<build><plugins>` section:

```xml
            <plugin>
                <groupId>net.bytebuddy</groupId>
                <artifactId>byte-buddy-maven-plugin</artifactId>
                <version>1.18.1</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>transform</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <skip>${syncause.disable}</skip>
                    <transformations>
                        <transformation>
                            <plugin>com.syncause.bytebuddy.plugin.SyncausePlugin</plugin>
                            <arguments>
                                <argument><index>0</index><value>wss://api.syn-cause.com/codeproxy/ws</value></argument>
                                <argument><index>1</index><value>{apiKey}</value></argument>
                                <argument><index>2</index><value>${syncause.disable.profiles}</value></argument>
                                <argument><index>3</index><value></value></argument>
                                <argument><index>4</index><value>{appName}</value></argument>
                                <argument><index>5</index><value>{projectId}</value></argument>
                            </arguments>
                        </transformation>
                    </transformations>
                </configuration>
            </plugin>
```

## Step 5: Build & Run
```bash
mvn clean package
# Restart the application
```
