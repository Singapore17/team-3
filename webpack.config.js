var webpack=require('webpack');

module.exports = {
     entry: './foodbank/static/js/index.js',
     output: {
         path: './foodbank/static/bundle/',
         filename: 'bundle.js'
     },
     module: {
         loaders: [{
             test: /\.js$/,
             exclude: /node_modules/,
             loaders: ['babel-loader', 'eslint-loader']
         },
         { test: /\.css$/, loaders: ["style", "css"] },
         {test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: 'file'},
        {test: /\.(otf|woff|woff2)$/, loader: 'url-loader?prefix=font/&limit=5000'},
        {test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=application/octet-stream'},
        {test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=image/svg+xml'}
         ]
     }
 }

