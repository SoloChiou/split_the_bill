module.exports = {
  devServer: {
    host: "0.0.0.0", // 使服务器绑定到所有网络接口
    port: 8080,
    watchOptions: {
      poll: true,
    },
  },
  outputDir: "dist",
};
