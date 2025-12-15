import { VStack, Box, Text, Link } from "@chakra-ui/react";
import ChatBubble from "./ChatBubble";
import type { ChatAreaProps } from "../interfaces";

const ChatArea = ({ messages,
  onCitationClick,
  isSearching,
  searchingIndicator }: ChatAreaProps) => {
  return (
    <Box flex="1" overflowY="auto" p={4} background="#3737374b" data-chat-area>
      <VStack align="stretch">
        {messages.length === 0 &&
          <div style={{
            display: 'flex',
            flexDirection: 'column', marginTop: '9rem', justifyItems: 'center', alignItems: 'center'
          }}>
            {/* <Box as="ul" style={{
              display: 'flex', flexDirection: 'column',
              gap: '1rem', fontFamily: 'cursive', fontSize: '1.3rem',
              overflowWrap: 'break-word', animation: 'ease-in-out'
            }} color={'teal.400'} listStyleType={'revert'}>
              <Text animation='ease-in-out' backgroundColor={'red.900'} borderRadius={'2xl'} maxWidth={'max-content'}>
                This is a Stateless System hence we do not Store Your API Key in the Server.
              </Text>
              <Text animation='ease-in-out' backgroundColor={'yellow.900'} borderRadius={'2xl'} maxWidth={'max-content'}>
                The MultiQuery and Decomposition Search can only be used with a valid Gemini Key.
              </Text>
              <Text animation='ease-in-out' backgroundColor={'orange.900'} borderRadius={'2xl'} maxWidth={'max-content'}>
                The system uses an extra API Call per query to verify if the Key Provided is Authentic or not.
              </Text>
            </Box> */}
          </div>

        }
        {messages.map((msg, idx) => (
          <Box key={idx}>
            <ChatBubble
              message={msg.text}
              queries_={msg.queries}
              sender={msg.sender}
              sources={msg.sources}
            />
            {msg.citations && msg.citations.length > 0 && (
              <Box mt={1} ml={2}>
                <Text fontSize="sm" color="gray.300">
                  Citations:
                </Text>
                {msg.citations.map((c, j) => (
                  <Link
                    key={j}
                    color="teal.300"
                    ml={2}
                    cursor="pointer"
                    onClick={() => onCitationClick(c.page, c.file)}
                  >
                    {c.text}
                  </Link>
                ))}
              </Box>
            )}
          </Box>
        ))}
        {isSearching && searchingIndicator}
      </VStack>
    </Box >
  );
};

export default ChatArea;
