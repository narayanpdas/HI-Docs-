import { HStack, Input, IconButton, Switch } from "@chakra-ui/react";
import { useState } from "react";
import { FiSend } from "react-icons/fi";
// import UploadButton from "./UploadButton";
import { TbWorld } from "react-icons/tb";
import SearchSpace from "./utils/SearchSpace"
const ChatInput = ({ onSend, keyingest }: { onSend: (msg: string, top_n: number) => void, keyingest: string }) => {
  const [text, setText] = useState("");
  const [internetOn, setInternetOn] = useState(true);
  const [currentTopN, setCurrentTopN] = useState(3);
  const handleTopNChange = (top_n: number) => {
    setCurrentTopN(top_n);
    console.log("ChatInput received new top_n:", top_n);
  };
  const handleSend = () => {
    if (text.trim()) {
      onSend(text, currentTopN);
      setText("");
    }
  };
  return (
    <HStack p={3} bg="#333333ff" width={'93%'} margin={'0rem 2.5rem'}
      alignSelf={'center'} borderRadius={'1rem'}  >
      <Switch.Root>
        <Switch.HiddenInput />
        <Switch.Control onChange={() => setInternetOn(!internetOn)} />
        <Switch.Label ><TbWorld size={24} /></Switch.Label>
      </Switch.Root>
      <Input
        placeholder="Type a message..."
        borderRadius={'2rem'}
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
      />
      <SearchSpace onTopNChange={handleTopNChange} keyingest={keyingest} />
      <IconButton aria-label="Send" colorScheme="blue" onClick={handleSend}>
        <FiSend />
      </IconButton>
    </HStack>
  );
};

export default ChatInput;
