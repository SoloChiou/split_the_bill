module.exports = {
  devServer: {
    watchOptions: {
      poll: true,
    },
    // 使 Docker 容器可以通過主機訪問
    host: "0.0.0.0",
    // Nginx port
    port: 80,
  },
  outputDir: "dist",
};
