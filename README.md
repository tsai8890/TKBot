
<h1 align="center">
  <br>
  TKBot
  <br>
</h1>

<h4 align="center">A TKB booking app built on top of Selenium.</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#usage">Usage</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#contact">Contact</a> •
  <a href="#acknowledgments">Acknowledgments</a>
</p>


<!-- KEY FEATURES -->
## Key Features

* Auto Booking
  - Immediately book the seats after the offical website refresh the opening seats at 00:00.
  - After reserving through the app, you can leave it alone.
* Auto Login
  - Automatically login when you launch the app, after you set up the config by your own username and passowrd
* Multiple Sessions
  - You can select more than one sessions, and the app will book all of them as more as possible


<!-- GETTING STARTED -->
## Getting Started

<!-- ### Prerequisites -->

### Installation

1. Clone the repo
    ```bash
    $ git clone https://github.com/tsai8890/TKBot.git
    ```
2. Install python packages
    ```
    $ cd TKBot/src
    $ pip3 install -r requirements
    ```
3. Copy the config template
    ```
    $ cd TKBot/src
    $ cp .env.default .env
    ```
4. Enter your username and password in .env
    ```env
    username=[your username]
    password=[your password]
    ```



<!-- USAGE -->
## Usage



<!-- ROADMAP -->
## Roadmap

- [x] Add a simple GUI interface
- [ ] Add a `update tkb data` button into the GUI interface
  - [x] update function
  - [ ] update button
- [ ] Support multiple users at once



<!-- CONTRIBUTING -->
## Contributing



<!-- CONTACT -->
## Contact

Peter Tsai - asdpeter6520@gmail.com

Project Link: [https://github.com/tsai8890/TKBot](https://github.com/tsai8890/TKBot)



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments