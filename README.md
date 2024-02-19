# LINE_chatbot
<div id="top"></div>


<!-- PROJECT LOGO -->
<br />
<div align="center">
 

  <h1 align="center">HamaPfy</h1>

  <p align="center">
    Music service like Spotify created by Toshiya Hama  and Hayato Shimizu(P)</br>
    濱(Hama)と清水(P)が作ったSpotifyみたいな名前の音楽サービス
 <!--   <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
  -->
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
       <li><a href="#built-with">Built With</a></li>
        <li><a href="#tree">Tree</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>




## About The Project
<div align="center">
 <img src="static/images/talkimage1.jpg" width="250" alt="demo" title="demo">
 <img src="static/images/talkimage2.jpg" width="250" alt="demo" title="demo">
 <img src="static/images/talkimage3.jpg" width="250" alt="demo" title="demo">
</div>
<!-- 
[![Product Name Screen Shot][product-screenshot]](https://example.com)

There are many great README templates available on GitHub; however, I didn't find one that really suited my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need -- I think this is it.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should implement DRY principles to the rest of your life :smile:

Of course, no one template will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. Thanks to all the people have contributed to expanding this template!

Use the `BLANK_README.md` to get started.

<p align="right">(<a href="#top">back to top</a>)</p> -->

### Built With
* [Python](https://www.python.org/)
* [Flasek](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/index.html)
* [Heroku](https://devcenter.heroku.com/)


### Tree
```
.
├── Procfile
├── README.md
├── app.py
├── db_handler.py
├── music.sql
├── requirements.txt
├── runtime.txt
├── static
│   ├── images
│   │   ├── hamaPfyQRcode.png
│   │   ├── hamaPfyQRcode.png:Zone.Identifier
│   │   ├── talkimage1.jpg
│   │   ├── talkimage2.jpg
│   │   └── talkimage3.jpg
│   └── style.css
├── templates
│   └── index.html
└── youtube_utils.py
```
<!-- 
This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [Next.js](https://nextjs.org/)
* [React.js](https://reactjs.org/)
* [Vue.js](https://vuejs.org/)
* [Angular](https://angular.io/)
* [Svelte](https://svelte.dev/)
* [Laravel](https://laravel.com)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com) -->

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
<!-- This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps. -->

### Prerequisites

<b>requirements.txt</b>
```
Flask==2.1.2
line-bot-sdk==2.2.1
psycopg2-binary==2.9.3
pytube==12.1.0
```

<!-- This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ``` -->

### Installation

1. 下記添付サイトに従って、herokuのアカウント登録を行う。

- [Getting Started on Heroku with Python | Heroku Dev Center](https://devcenter.heroku.com/articles/getting-started-with-python "Getting Started on Heroku with Python | Heroku Dev Center")
</br>

2. LINE Developersにて、アカウントの作成を行う。
- [LINE Developers](https://developers.line.biz/en/ "a")
</br>

3. コマンドプロンプトにて任意のディレクトリに移動し、リポジトリをクローンする。
```
$ git clone https://github.com/Hayato-7812/LINE_chatbot.git
```
 ### References
- [Webアプリ初心者のFlaskチュートリアル - Qiita](https://qiita.com/kro/items/67f7510b36945eb9689b "a")



<!-- _Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._
 -->
<!-- 1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ``` -->

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
1. <b>自分の好きな音楽を共有する！</b>
- メニュー左のボタンを押して「Share songs with others!」と送信
- Please input YouTube linkon the keyboard!!」と出るのでYouTubeリンクを送信
- 共有完了！
　
2. <b>他の人のおすすめの音楽が知りたい！</b>
- メニュー中央のボタンを押して「What are other people's favorite songs?」と送信
- 他の人がおすすめした音楽が表示される！
<!-- Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_ -->

<p align="right">(<a href="#top">back to top</a>)</p>



## Contact

<!-- Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name) -->

<p align="right">(<a href="#top">back to top</a>)</p>

