import axiosInstance from "./axiosInstance";
import type{ AxiosProgressEvent } from 'axios';
export const initToken = async () => {
  try{
    const token = localStorage.getItem("token")
    if (token === null){
      localStorage.setItem("token","3");
    }
  }
  catch (err) {
      console.error(err);
      alert("token issue Failed please Refresh");
      return err;
  }
};
export const useToken = async() =>{
  const token = localStorage.getItem("token");
  if (token){
    let x:number = parseInt(token) - 1;
    localStorage.setItem("token",x.toString());
  }
}
export const getToken = async()=>{
  return localStorage.getItem("token");
}
export const getKey = async()=>{
  return sessionStorage.getItem("apikey");
}
export const removeKey = async()=>{
  return sessionStorage.removeItem("apikey");
}
export const get_docs = async () => {
    try{
      const res = await axiosInstance.get("/docs");
      return res;
    }
    catch(err){
      console.error(err);
      alert("Failed! No Server to Fetch");
    }
}
interface apitoken {
  token?:string | null,
  api_key?:string | null
}
export const send_token = async (data:apitoken)=>{
  try{
    console.log("data",JSON.stringify(data));
    const res = await axiosInstance.post<apitoken>('/create',data);
    return res;
  }
  catch(err){
      console.error(err);
      console.log("Failed! To create User please Refresh!");
  }
}

export const checkStatus = async ()=>{
  try{
    const res = await axiosInstance.get('/status');
    console.log(res.data);
    return res.data;
  }
  catch(err){
    console.error(err);
  }
}
export const fileUpload = async (file:File,onProgress?:(percent:number)=>void)=>{
  const formData = new FormData();
  formData.append('file',file);
  try{
    const response = await axiosInstance.post('/upload',formData,
      {
        onUploadProgress:(progressEvent: AxiosProgressEvent)=>{
          if (progressEvent.total){
            const percentCompleted = Math.round(
              (progressEvent.loaded *100) / progressEvent.total
            );
          if (onProgress) {
            onProgress(percentCompleted);
            }
          } 
        }
      }
    
    );
    console.log("Uploaded the damm PDf", response.data);
    return response.data;
  }
  catch(err){
    console.log("We Fu**ed Up, Here is the Error for while uploading file:",err)
  }
}
