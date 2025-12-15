import { Flex, Box, Text, Spinner } from "@chakra-ui/react";
import { useState, useEffect } from "react";
import ChatArea from "./components/ChatArea";
import ChatInput from "./components/ChatInput";
import PdfViewer from "./components/Pdfviewer";
import "./styles/chat_page.css";
import { stream_message } from "./services/chatService";
import type { ChatMessage } from "./interfaces";
import { CgCloseO } from "react-icons/cg";
import SearchingIndicator from "./components/utils/searching";
import Filedock from "./components/Filedock";
import ApiPopup from "./components/ApiPopup";
import {
  send_token, get_docs, initToken,
  useToken, getToken, getKey, removeKey,
  checkStatus
} from "./services/authService";
import create_token from './auth/Createtoken';


const ChatPage = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [pdfLink, setPdfLink] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [isSearching, setIsSearching] = useState<boolean>(false);

  const [docLoading, setDocLoading] = useState(false);
  const [docs, setDocs] = useState<any[] | false>(false);
  const [fileStatus, setFileStatus] = useState(true);
  const [checkedDocs, setCheckedDocs] = useState<{ [key: string]: boolean }>({});
  const [apiingest, setapi] = useState<string>("");

  useEffect(() => {
    const stat = async () => {
      const res = await checkStatus();
      console.log(res.data);
      if (res.data && res.data.message !== "success") {
        setFileStatus(false);
      }
    }
    if (docs === false) {
      create_token();
      setDocLoading(true);
      handle_fetch_docs();
      initToken();
      console.log(sessionStorage.getItem('user_token'));
      const api_key = sessionStorage.getItem('api_key');
      stat();
      send_token({
        token: sessionStorage.getItem('user_token'),
        api_key: (api_key === null) ? "" : api_key
      });
      stat();
    }
  }, [docs]);
  useEffect(() => {
    if (docs && docs.length > 0) {
      const inital_ticks: { [key: string]: boolean } = {};
      docs.forEach(doc => { inital_ticks[doc.id] = true; });
      setCheckedDocs(inital_ticks);
    } else if (docs === false) {
      setCheckedDocs({});
    }
  }, [docs]);
  const changeapi = (value: string) => {
    setapi(value);
    console.log(value);
    send_token({ token: sessionStorage.getItem('user_token'), api_key: value });
  }
  const handleSelectAll = () => {
    if (!docs || docs.length === 0) return;
    const newTicks: { [key: string]: boolean } = {};
    docs.forEach(doc => { newTicks[doc.id] = true; });
    setCheckedDocs(newTicks);
  };
  const handleClearAll = () => {
    if (!docs || docs.length === 0) return;
    const newTicks: { [key: string]: boolean } = {};
    docs.forEach(doc => { newTicks[doc.id] = false; });
    setCheckedDocs(newTicks);
  };
  const handleSend = async (msg: string, top_n: number = 3,) => {
    setMessages((prev) => [...prev, { text: msg, sender: "user" }]);
    const tickedIds = Object.keys(checkedDocs).filter(id => checkedDocs[id]);
    const filters = { "doc_ids": tickedIds };
    let token = await getToken();
    let apikey = await getKey();
    console.log(apikey, tickedIds.length)
    console.log(token);
    if (tickedIds.length == 0) {
      setMessages((prev) => [...prev, { text: `No Files Selected`, sender: "bot" }]);
    }
    else if ((apikey == null || apikey === "") && (token === null || parseInt(token) <= 0)) {
      setMessages((prev) => [...prev, { text: `Limit Reached please use Your personal API key for more `, sender: "bot" }]);
    }
    else {
      try {
        const update_message = (data: any) => {
          if (data.type === 'status') {
            setIsSearching(true);
            setTimeout(() => {
              const chatArea = document.querySelector('[data-chat-area]');
              chatArea?.scrollTo({ top: chatArea.scrollHeight + 1, behavior: 'smooth' });
            }, 0);
          }
          else if (data.type === "thought") {
            useToken();
            const clean_text = (data: string[]) => {
              for (let i = 0; i < data.length; i++) {
                const new_data = data[i].replace(/#\d+/g, "")
                data[i] = new_data;
              }
              return data;
            }
            setMessages((prev) => [...prev, { text: ``, queries: clean_text(data.content), sender: "bot" }]);
            setTimeout(() => {
              const chatArea = document.querySelector('[data-chat-area]');
              chatArea?.scrollTo({ top: chatArea.scrollHeight, behavior: 'smooth' });
            }, 0);
          }
          else if (data.type === "source") {
            // let all_search_results = "";
            // console.log("data: ", data.content)
            // for (let i = 0; i < data.content.length; ++i) {
            //   all_search_results += data.content[i]
            // }
            // const search_results = JSON.parse(all_search_results.replace(/'/g, '"'))
            // let resultss: string[] = [];
            // for (let i = 0; i < search_results.length; ++i) {
            //   let _temp = (search_results[i].toString()) + '\n'
            //   // search_results[i] = _temp + '\n'
            //   resultss.push(_temp)
            // }
            console.log(JSON.parse(data.content))
            setMessages((prev) => [...prev, { text: ``, sources: JSON.parse(data.content), sender: "bot" }]);
            setTimeout(() => {
              const chatArea = document.querySelector('[data-chat-area]');
              chatArea?.scrollTo({ top: chatArea.scrollHeight, behavior: 'smooth' });
            }, 0);
          }
          else if (data.type === "llm") {
            setMessages((prev) => [...prev, { text: `${data.content}`, sender: "bot" }]);
            setTimeout(() => {
              const chatArea = document.querySelector('[data-chat-area]');
              chatArea?.scrollTo({ top: chatArea.scrollHeight + 1, behavior: 'smooth' });
            }, 0);
          }
          else if (data.type === "final") {
            setIsSearching(false);
            setTimeout(() => {
              const chatArea = document.querySelector('[data-chat-area]');
              chatArea?.scrollTo({ top: chatArea.scrollHeight + 1, behavior: 'smooth' });
            }, 0);

          }
          else if (data.type === "error") {
            setMessages((prev) => [...prev, { text: `⚠️ Some Error Occured`, sender: "bot" }]);
            setIsSearching(false);
          }
          else if (data.type === "nofiles") {
            setMessages((prev) => [...prev, { text: `No Files Selected`, sender: "bot" }]);
            setIsSearching(false);
          }
          else if (data.type === "invalid_api_key") {
            setMessages((prev) => [...prev, { text: `Please provide a valid API KEY`, sender: "bot" }]);
            setIsSearching(false);
            removeKey();
            changeapi("");
          }
        };
        if (apikey) {
          stream_message({ query: msg, top_n: top_n, filters: filters }, update_message);
        }
        else stream_message({ query: msg, top_n: top_n, filters: filters }, update_message);
      }
      catch (error) {
        console.log(error);
        setMessages((prev) => [...prev, { text: "Some Error has Occured Please wait!", sender: "bot" }]);
        setIsSearching(false);
        return {}
      }
      finally {
        setIsSearching(false);
      }
    }
  };
  const handlecheckchange = (id: string | number) => {
    setCheckedDocs(prevTicks => ({
      ...prevTicks,
      [id]: !prevTicks[id]
    }));
  };
  const handle_fetch_docs = async () => {
    try {
      console.log("Requesting server for docs...");
      const documents = await get_docs();
      if (documents && documents.data) {
        console.log(documents.data)
        setDocs(documents.data);
      } else {
        setDocs([]);
      }
    } catch (err) {
      console.log(err);
      setDocs([]);
    } finally {
      setDocLoading(false);
    }
  };
  const handleRefresh = () => {
    setDocs(false);
  }
  return (
    <Box className="chat_page_">
      <Flex h={"100%"} direction="row" flex="2" zIndex="40">
        <Flex direction="column" flex="2">
          <Flex background="#3737374b" display={"flex"} gap={'2'} >
            <Filedock
              docs={docs}
              loading={docLoading}
              checkedDocs={checkedDocs}
              onCheckChange={handlecheckchange}
              onRefresh={handleRefresh}
              onSelectAll={handleSelectAll}
              onClearAll={handleClearAll}
            />
            <ApiPopup setapi={changeapi} />
            <Text alignSelf={'center'}
              marginRight={'20px'} marginLeft={'auto'}
              font={'caption'} fontSize={'2xl'}
            >
              HI Docs
            </Text> {/* Highly Intelligent Docs */}
          </Flex>
          {!fileStatus &&
            <Box justifyItems={'center'}
              marginTop={'20%'}>
              <div style={{ display: 'flex', flexDirection: 'row', gap: '0.5rem' }}>
                <Text colorPalette={'teal.200'}>Processing File...</Text>
                <Spinner colorPalette={'teal'} />
              </div>
            </Box>
          }
          {fileStatus &&
            <>
              <ChatArea
                messages={messages}
                onCitationClick={(page, file) => {
                  setCurrentPage(page);
                  if (!pdfLink) setPdfLink(`/${file}`);
                }}
                isSearching={isSearching}
                searchingIndicator={<SearchingIndicator />}
              />
              <Flex bg={"#3737374b"} margin={"3px"}>
                <ChatInput onSend={handleSend} keyingest={apiingest} />
              </Flex>
            </>
          }
        </Flex>
        {pdfLink && (
          <Box
            flex="1"
            h="100vh"
            overflow="hidden"
          >
            <Box
              position="absolute"
              top="10px"
              right="10px"
              bg="red.600"
              color="white"
              borderRadius="1rem"
              cursor="pointer"
              _hover={{ bg: "red.700" }}
              onClick={() => setPdfLink(null)}
              zIndex={50}
            >
              <CgCloseO size={'1.5rem'} />
            </Box>
            <PdfViewer fileUrl={pdfLink} page={currentPage} />
          </Box>
        )}
      </Flex>
    </Box>
  );
};
export default ChatPage;