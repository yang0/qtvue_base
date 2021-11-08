const path = require('path')

function resolve(dir) {
    return path.join(__dirname, dir)
  }

module.exports = {
    publicPath: './',
    lintOnSave: process.env.NODE_ENV === 'development',
    pages: {
        index: {
            entry: 'src/page/index/main.js',
            template: 'public/index.html',
            filename: 'index.html',
            title: 'index page'
        },
        iconbar: {
            entry: 'src/page/iconbar/main.js',
            template: 'public/index.html',
            filename: 'iconbar.html',
            title: 'iconbar page'
        }
    },

    configureWebpack: {
        // provide the app's title in webpack's name field, so that
        // it can be accessed in index.html to inject the correct title.
        resolve: {
          alias: {
            '@': resolve('src')
          }
        }
      },

}