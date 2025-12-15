//NOTE: Secondary interfaces required by the Primary (not used directly).
export interface RecieveMessageLLM{
    context_answer: string;
    summary: string;
    citation: string[];
}

//NOTE: These are Primary interfaces Directly used across all Files for safe data sending 
//      and recieving operations.

// Authentication Interfaces
export interface UserLoginRequest{
    username:string;
    password:string;
}
export interface UserRegisterRequest{
    username:string;
    email:string;
    password:string;
}
export interface UserLoginResponse{
    access_token: string;
    token_type: string;
    username: string;
    id: number;
}
export interface UserRegisterResponse{
    email:string;
    username:string;
    role:string;
}

// ChatArea Interfaces
export interface SendMessage{
    query: string;
    top_n?: number;
    filters?: {doc_ids:string[]};
    // api_key?:string;
}
export interface RecieveMessage{
    chad_id:number;
    user_query:string;
    llm_response:RecieveMessageLLM[];
}

export interface AuthContextType {
  role: "ADMIN" | "VIEWER" | null;
  setRole: (role: "ADMIN" | "VIEWER") => void;
}
export interface ChatMessage {
  text: string;
  sender: "user" | "bot";
  citations?: { text: string; page: number; file: string }[];
  queries?:string[];
  sources?:string[];
}

export interface ChatAreaProps {
  messages: ChatMessage[];
  onCitationClick: (page: number, file: string) => void;
  isSearching?: boolean;
  searchingIndicator?: React.ReactNode;
}

export interface Doclist{
    id:number;
    name:string;
    path:string;
}





