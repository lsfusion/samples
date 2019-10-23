# lsfusion-samples

[project]:https://github.com/mazzy-ax/lsfusion-samples
[license]:https://github.com/mazzy-ax/lsfusion-samples/blob/master/LICENSE

<img alt="logo" src="https://lsfusion.org/themes/lsfusion/assets/images/i-logo-lsfusion.svg" align="right">

Примеры для демонстрации возможностей платформы `lsFusion`.

<https://documentation.lsfusion.org/pages/viewpage.action?pageId=2228236>

Проект [lsfusion-samples][project] должен упростить жизнь тем, кто только начал знакомиться с `lsFusion`.
Предполагается, что перед началом работы с примерами вы запускаете сервисы одной командой `docker-compose`,
а дальше работаете только внутри `IntelliJ IDEA`.

Причем проект устроен так, что вам не нужно изучать и использовать maven-команды,
достаточно переключать и запускать конфигурации в `IntelliJ IDEA`.

## Необходимо установить (prerequisites)

Предполагается, что вы уже установили на свой компьютер:

* `git`
* `docker` и `docker-compose`
* `IntelliJ IDEA`, достаточно Community Edition
* `lsFusion plugin` для IntelliJ IDEA
* (опционально) `Docker plugin` для IntelliJ IDEA
* `java8` или более поздние версии
* (опционально) `lsfusion2-client` для запуска web-клиента lsFusion
* (опционально) `IceTea Web Control` для запуска desktop-клиента lsFusion по jnlp-ссылке
* (опционально) `jar-файл` с desktop-клиентом lsFusion

Отдельный `lsfusion2-server` можно не устанавливать, поскольку в данном проекте сервер `lsFusion` запускается из IDEA.

### git

Инструкции по установке можно найти здесь <https://git-scm.com/download/>.

### docker и docker-compose

Инструкции по установке можно найти здесь:

* <https://docs.docker.com/install/>
* <https://docs.docker.com/compose/install/>

### IntelliJ IDEA

Инструкции по установке можно найти здесь <https://www.jetbrains.com/idea/download>.

* Примечание 1: Для работы с демонстрационными примерами достаточно установить `Community Edition`.
* Примечание 2: На Ubuntu `IDEA Community Edition` можно найти в штатной утилите `Ubuntu software`
или установить безо всяких заморочек через `snap`:

```
sudo snap install intellij-idea-community --classic 
```

### lsFusion plugin для IntelliJ IDEA

Чтобы установить [lsFusion plugin](https://plugins.jetbrains.com/plugin/7601-lsfusion/):

* в `IDEA` откройте File \ Settings \ Plugins
* Найдите плагин `lsFusion` и нажмите `Install`  

### Docker plugin для IntelliJ IDEA

[Docker plugin](https://plugins.jetbrains.com/plugin/7724-docker/) уже включен в `Ultimate edition`.
В `IDEA Community edition` его нужно установить:

* в `IDEA` откройте File \ Settings \ Plugins
* Найдите плагин `Docker` и нажмите `Install`  

### java8 или более поздние версии

Инструкции по установке можно найти здесь <https://www.java.com>

* Примечание: в Ubuntu достаточно команды:

```
sudo apt install default-jdk
```

### (опционально) lsfusion2-client

*Важно: Перед установкой `lsfusion2-client` необходимо установить java8+.* 

Как ни странно, `lsfusion2-client` - это сервер, который работает как служба/демон, внутри которого работает обычный [tomcat](https://tomcat.apache.org/):
* слушает порт 8080
* перенаправляет запросы серверу `lsFusion` на порт 7652 (в данном проекте сервер `lsFusion` запускается из IDEA)
* возвращает ответ в виде html

Инструкция по установке:

* для [Windows](https://documentation.lsfusion.org/pages/viewpage.action?pageId=57738076)
* для [Linux](https://documentation.lsfusion.org/pages/viewpage.action?pageId=57738078)

Так выглядят команды для установки `lsfusion2-client` на `Ubuntu`:

```
# Import lsFusion GPG Key
wget --quiet -O - https://download.lsfusion.org/apt/GPG-KEY-lsfusion | sudo apt-key add -

# Install lsFusion repo
sudo apt-add-repository "deb https://download.lsfusion.org/apt all main"

# Install lsFusion server and client
sudo apt install -y lsfusion2-client
```

### (опционально) IceTea Web Control

[IceTea Web Control](https://icedtea.classpath.org/wiki/IcedTea-Web) &mdash; это проект, который позволяет запускать
Java-апплеты при помощи jnlp-ссылок.

Когда билд `lsFusion` модуля подходит к концу, в log пишется jnlp-ссылка
на desktop-клиента. Если нажать на нее, то `IceTea Web Control` автоматически запустит desktop-клиент.

Инструкции по установке можно найти на сайте проекта [IceTea Web Control](https://icedtea.classpath.org/wiki/IcedTea-Web).
На Ubuntu можно найти и установить в штатной утилите `Ubuntu software`. 

Вы можете убрать назойливый splash, задав переменные окружения:

```
ICEDTEA_WEB_PLUGIN_SPLASH=none
ICEDTEA_WEB_SPLASH=none
```   

Если не установить `IceTea Web Control`, то desktop-клиент нужно будет запускать вручную.

### (опционально) jar-файл

Desktop-клиент `lsFusion` версии 2.1 можно скачать по ссылке: <https://download.lsfusion.org/java/lsfusion-client-2.1.war>

Остальные версии клиента можно найти по ссылке: <https://download.lsfusion.org/java/>

## Как запустить демонстрационный пример

Прежде всего склонируйте проект на свой компьютер при помощи git:

```
$ git clone https://github.com/mazzy-ax/lsfusion-samples.git
```

1. войдите в каталог проекта `lsfusion-samples`
2. запустите команду `docker-compose` чтобы запустить сервер базы данных

```
$ cd lsfusion-samples
$ docker-compose up -d
```

3. откройте каталог проекта в `IntelliJ IDEA`, разрешите maven'у открыть pom.xml и синхронизировать зависимости
4. выберите конфигурацию с примером. Например, `lsFusion server: hockeystats` (Run \ Edit configurations...)
5. запустите эту конфигурацию (Run \ Run 'lsFusion server: hockeystats')
6. запустите клиента:
   * если у вас установлен `lsfusion2-client`, то откройте в браузере страницу по адресу `http://localhost:8080`
   * если у вас установлен `IceTea Web Control`, то кликните на jnlp-ссылку, которая появится в конце лога в информационном окне `Run`
   * или запустите `jar-файл` с desktop-клиентом lsFusion

## Как запустить pgadmin

1. войдите в каталог проекта `lsfusion-samples`
2. запустите команду `docker-compose` чтобы запустить сервер базы данных
3. откройте в браузере страницу по адресу `http://localhost:5050`
4. в первый раз `pgadmin` спросит email и пароль администратора pgadmin
   * введите email: `pgadmin4@pgadmin.org`
   * введите пароль: `11111`
5. в первый раз `pgadmin` автоматически добавит сервер с базой данных и попросит пароль администратора `postgres`
   * введите пароль: `11111`
   * если хотите, установите галочку `Save password`

