module.exports = {
  devServer: {
    disableHostCheck: true,
    host: "0.0.0.0",
    port: 8080,
    watchOptions: {
      poll: true,
    },
  },
  outputDir: "dist",
};
