const path = require('path');

const devMode = process.env.NODE_ENV !== 'production';

module.exports = {
    entry: [
        './dist/js/app.js',
    ],
    output: {
        path: path.resolve(__dirname, 'static/js'),
        filename: 'app.js',
    },
};
