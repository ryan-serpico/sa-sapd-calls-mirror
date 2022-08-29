<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
    <div style='font-size: 5rem;' >🤖</div>

<h3 align="center">sa-sapd-calls-mirror</h3>

  <p align="center">
    A full record of SAPD's calls for service.
    <br />
    <br />
    <a href="https://flatgithub.com/ryan-serpico/sa-sapd-calls-mirror/blob/main/output/archive.csv">View Data</a>
    ·
    <a href="https://github.com/ryan-serpico/sa-sapd-calls-mirror/issues">Report Bug</a>
    ·
    <a href="https://github.com/ryan-serpico/sa-sapd-calls-mirror/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <!-- <li><a href="#usage">Usage</a></li> -->
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
[![Product Name Screen Shot][product-screenshot]](https://www.expressnews.com/)
**TL;DR:** This bot updates [an archive](https://github.com/ryan-serpico/sa-sapd-calls-mirror/blob/main/output/archive.csv) of [calls to service to the San Antonio Police Department](https://www.sanantonio.gov/SAPD/Calls). The aim is to provide a full and accessible record of calls to service to SAPD.

The San Antonio Police Department (SAPD) maintains two dashboards that provide a record of calls to service. One for [historical calls](https://webapp3.sanantonio.gov/policecalls/Reports.aspx) and another [focused on the last seven days](https://experience.arcgis.com/experience/7204b710e882450e9cf0f5d78334cc59) (updated once a week).

The historical calls web app is problematic because it can only return 10,000 call records at a time. If you want to look at these data over time for each ZIP code area around San Antonio going back ten years, you're going to have to click through thousands of forms. And even if you were to do that, there is an issue with the web app where it doesn't spit out the the data in a format accessible to the public when you click the "Export to Excel." button. It downloads a .aspx file instead.

The dashboard dedicated to the last seven days has something that the historical calls database doesn't have: call coordinates. This is useful for performing spatial analysis on the data. Unfortunately, the there is no way for the public to access this data.

*Enter this bot*. It checks for new calls to service listed in the dashboard dedicated to the last seven days and adds them [to an archive](https://github.com/ryan-serpico/sa-sapd-calls-mirror/blob/main/output/archive.csv).

This means that in the future, you won't need to go to SAPD's website to pull data. You can just check the archive here and download everything in its entirety.

**Note:** SAPD makes clear that this data are not crimes but calls for service. 

> Police Calls for service reflect each time someone called the police for service.  These are CALLS FOR SERVICE, NOT Lists of Crimes or Crime Reports. Calls are titled as they are called in and dispatched. For example, a call may be dispatched as a "robbery", as called in by a citizen, but later the officer finds it is a "burglary." This would be listed in the Calls for Service report as a "robbery".

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* ![Python][python]
* ![Pandas][pandas]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
If you want to run this code locally, here you go.

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/ryan-serpico/sa-sapd-calls-mirror.git
   ```
2. Install packages
   ```sh
   pip3 install -r requirements.txt
   ```
3. Run the bot
   ```sh
   python3 app.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
<!-- ## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- ROADMAP -->
## Roadmap

- [ ] Add calls for service prior to August 17, 2022 to archive.csv.

See the [open issues](https://github.com/ryan-serpico/sa-sapd-calls-mirror/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.md` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Ryan Serpico - [@ryan_serpico](https://twitter.com/ryan_serpico) - ryan.serpico@express-news.net.com

Project Link: [https://github.com/ryan-serpico/sa-sapd-calls-mirror](https://github.com/ryan-serpico/sa-sapd-calls-mirror)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Taylor Pettaway](https://www.expressnews.com/author/taylor-pettaway/) for giving me a reason to finally do this.
* The [City of San Antonio](https://www.sanantonio.gov/)
* The [San Antonio Police Department](https://www.sanantonio.gov/SAPD/Calls)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ryan-serpico/sa-sapd-calls-mirror.svg?style=for-the-badge
[contributors-url]: https://github.com/ryan-serpico/sa-sapd-calls-mirror/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ryan-serpico/sa-sapd-calls-mirror.svg?style=for-the-badge
[forks-url]: https://github.com/ryan-serpico/sa-sapd-calls-mirror/network/members
[stars-shield]: https://img.shields.io/github/stars/ryan-serpico/sa-sapd-calls-mirror.svg?style=for-the-badge
[stars-url]: https://github.com/ryan-serpico/sa-sapd-calls-mirror/stargazers
[issues-shield]: https://img.shields.io/github/issues/ryan-serpico/sa-sapd-calls-mirror.svg?style=for-the-badge
[issues-url]: https://github.com/ryan-serpico/sa-sapd-calls-mirror/issues
[license-shield]: https://img.shields.io/github/license/ryan-serpico/sa-sapd-calls-mirror.svg?style=for-the-badge
[license-url]: https://github.com/ryan-serpico/sa-sapd-calls-mirror/blob/main/LICENSE.md
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/ryanserpico
[product-screenshot]: img/archive_ss.png
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[pandas]: https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white
