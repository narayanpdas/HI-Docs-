import axiosInstance from "./axiosInstance";
import type {SendMessage} from "../interfaces"

export const createWebSocket = (endpoint:string) => {
  const token = localStorage.getItem("token");
  const baseWsUrl = "ws://127.0.0.1:8000/api/v1/ws/"; //TODO :CHANGE DURING DEPLOYEMENT
  const url = `${baseWsUrl}${endpoint}?token=${token}`;
  const ws = new WebSocket(url);
  ws.onopen = () => console.log(` WebSocket connection established for ${endpoint}...`);
  ws.onclose = () => console.log(` WebSocket disconnected for ${endpoint}...`);
  ws.onerror = (err) => console.error(" WebSocket error:", err);
  return ws;
};
export const stream_message  = async(
  message:SendMessage,
  update_message:any
)=>{
    return new Promise((resolve, reject) => {
    const ws = createWebSocket("chat");
    ws.onopen = () => {
      // console.log(JSON.stringify(message));
      ws.send(JSON.stringify(message));
    };
    ws.onmessage = (event) => {
      try {
        console.log("Connecting to Server...")
        const data = JSON.parse(event.data);
        update_message({type:data.type,content:data.value});
        if (data.type==='invalid_api_key' || data.type === 'final' || data.type === 'error'){
          ws.close()
        }
        resolve(data)
      } 
      catch (err) {
        reject(err);
      }
    };
    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
      reject(err);
    };
    ws.onclose = () => {
      console.log("Connection closed");
    };
  });
};
export const sendmessage = async(message:SendMessage)=>{
    const res = await axiosInstance.post('/chat',message);
    return res.data
};