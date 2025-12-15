import axios from "axios";

const token = sessionStorage.getItem("user_token");
const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1/",
  params: {
    user_token:token
  }
});


// axiosInstance.interceptors.request.use(
//   (config) => {
//     const token = sessionStorage.getItem("user_token");
//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`;
//     }
//     return config;
//   },
//   (error) => Promise.reject(error)
// );

export default axiosInstance;
