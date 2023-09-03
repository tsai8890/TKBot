<a id="readme-top"></a>


<h1 align="center">
  <br>
  TKBot
  <br>
</h1>

<h4 align="center">A TKB booking app built on top of Selenium.</h4>

<p align="center">
  <a href="#about-the-project">About The Project</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#usage">Usage</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#contact">Contact</a> •
  <a href="#acknowledgments">Acknowledgments</a>
</p>
<br>


<!-- ABOUT THE PROJECT -->
## About The Project

### Key Features

* Auto Booking
  - Immediately book the seats after the offical website refresh the opening seats at 00:00.
  - After reserving through the app, you can leave it alone.
* Auto Login
  - Automatically login when you launch the app, after you set up the config by your own username and passowrd
* Multiple Sessions
  - You can select more than one sessions, and the app will book all of them as more as possible

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

<!-- ### Prerequisites -->

### Installation

1. Clone the repo
    ```bash
    git clone https://github.com/tsai8890/TKBot.git
    ```
2. Install python packages
    ```bash
    cd TKBot/src
    pip3 install -r requirements.txt
    ```
3. Copy the config template
    ```bash
    cd TKBot/src
    cp .env.default .env
    ```
4. Enter your username and password in .env
    ```env
    USERNAME=[your username]
    PASSWORD=[your password]
    ```
    
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE -->
## Usage
1. Run the app
    ```bash
    cd TKBot/src
    python3 main.py
    ```
<br>

2. After you launch the app, it will first try to login with your username and password

    <img src=images/readme/login.png width=700 height=400>
    
    > **Note**
    > If the login process is blocked by the website, then you would be required to login manually.

<br>

3. After the app successfully logged in, a window will pop up for the further reservation.

    <img src=images/readme/window_popup.png width=480 height=430>
<br>
  
4. Select each field, then click `預約`

    <img src=images/readme/window_reserve.png width=480 height=480>
<br>

5. After you click `預約`, it will show `已預約，等待中 ...`. You can change the reservation information before 00:00, after 00:00, the app will immediately book the specified sessions

    <img src=images/readme/reserve_waiting.png width=480 height=480>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add a simple GUI interface
- [ ] Add a `update tkb data` button into the GUI interface
  - [x] update function
  - [ ] update button
- [ ] Add a unique project icon
- [ ] Support multiple users at once

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing
<!-- Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. -->

If you have a suggestion that would make the project better, please fork the repo and create a pull request. <br> 
You can also simply open an issue with the tag `enhancement`. 

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<br>

Besides, if you find this project useful, don't forget to give it a star !

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Peter Tsai - asdpeter6520@gmail.com

Project Link: [https://github.com/tsai8890/TKBot](https://github.com/tsai8890/TKBot)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
* [Best README Template](https://github.com/othneildrew/Best-README-Template)
* [Electron-Markdownify's README](https://github.com/amitmerchant1990/electron-markdownify/blob/master/README.md)
* [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/#specification)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
