# android-keystore

build.gradle 설정

```groovy
// 키스토어 파일, 설정 확인
def keystoreFile = rootProject.file("keystore.jks")
def keystorePropertiesFile = rootProject.file("keystore.properties")
if (keystoreFile.exists() != keystorePropertiesFile.exists()) {
    if (!keystoreFile.exists()) {
        throw new GradleException("missing keystore.jks, if you do not want to use siging, please remove keystore.properties too.")
    }
    if (!keystorePropertiesFile.exists()) {
        throw new GradleException("missing keystore.properties, if you do not want to use siging, please remove keystore.jks too.")
    }
}

String keystorePassword = null
String debugPassword = null
String releasePassword = null
if (keystorePropertiesFile.exists()) {
    def keystoreProperties = new Properties()
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
    keystorePassword = keystoreProperties.getProperty('store')
    if (keystorePassword == null) {
        throw new GradleException("missing store password in keystore.properties")
    }
    debugPassword = keystoreProperties.getProperty('debug')
    if (debugPassword == null) {
        throw new GradleException("missing debug password in keystore.properties")
    }
    releasePassword = keystoreProperties.getProperty('release')
    if (releasePassword == null) {
        throw new GradleException("missing release password in keystore.properties")
    }
}

android {
    ...
    // 서명 정보가 있을 경우 추가
    signingConfigs {
        if (keystorePassword != null) {
            debug {
                storeFile keystoreFile
                storePassword keystorePassword
                keyAlias "debug"
                keyPassword debugPassword
                v1SigningEnabled true
                v2SigningEnabled true
            }
            release {
                storeFile keystoreFile
                storePassword keystorePassword
                keyAlias "release"
                keyPassword releasePassword
                v1SigningEnabled true
                v2SigningEnabled true
            }
        }
    }
    // 빌드시 적용
    buildTypes {
        debug {
            if (keystorePassword != null) {
                signingConfig signingConfigs.debug
            }
        }
        release {
            ...
            if (keystorePassword != null) {
                signingConfig signingConfigs.release
            }
        }
    }
}
```

서명 확인

```shell
# 전체 확인
keytool -list -printcert -jarfile app/build/outputs/apk/release/app-release.apk
# 서명 이름으로 동일한 인증서 확인
keytool -list -printcert -jarfile app/build/outputs/apk/release/app-release.apk | grep CN
```