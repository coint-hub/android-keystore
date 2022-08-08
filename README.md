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

String releasePassword = null
if (keystorePropertiesFile.exists()) {
    def keystoreProperties = new Properties()
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
    releasePassword = keystoreProperties.getProperty('key0')
    if (releasePassword == null) {
        throw new GradleException("missing release password in keystore.properties")
    }
}

android {
    ...
    // 서명 정보가 있을 경우 추가
    signingConfigs {
        if (releasePassword != null) {
            release {
                storeFile keystoreFile
                storePassword releasePassword
                keyAlias "key0"
                keyPassword releasePassword
                v1SigningEnabled true
                v2SigningEnabled true
            }
        }
    }
    // 빌드시 적용
    buildTypes {
        release {
            ...
            if (releasePassword != null) {
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