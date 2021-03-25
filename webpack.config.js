const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const devMode = process.env.NODE_ENV !== 'production';

module.exports = {
    mode: "production",

    entry: [
        './dist/js/app.js',
    ],
    output: {
        path: path.resolve(__dirname, 'static/js'),
        filename: 'app.js',
    },
};
