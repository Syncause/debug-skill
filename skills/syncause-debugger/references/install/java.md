# Syncause JAVA SDK Installation Guide

## Step 1: Add Profiles
In `pom.xml`, locate `<profiles>` and add:
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

## Step 2: Configure Repository
In `pom.xml`, ensure the following repository exists:
```xml
    <repositories>
        <repository>
            <id>github-syncause</id>
            <name>GitHub Packages</name>
            <url>https://syn-cause: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@maven.pkg.github.com/Syncause/syncause-sdk</url>
        </repository>
    </repositories>
```

## Step 3: Add Dependencies
In `pom.xml`, add the following before `</dependencies>`:
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
In `pom.xml`, add/update the `byte-buddy-maven-plugin` in `<plugins>`:
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
