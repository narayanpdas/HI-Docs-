import { Collapsible, Stack, Icon, Box, Text, Link, Flex, useCollapsible, Button } from "@chakra-ui/react";
import useTypewriter from "./utils/typewritter"
import ThinkingBubble from "./SearchingForbubble"
import SearchResults from "./SearchResults";
import { IoIosArrowDropright, IoIosArrowDropdown } from "react-icons/io";

const ChatBubble = ({ message, queries_, sender, sources, citations, onCitationClick }: {
  message: string,
  queries_?: string[],
  sender: "user" | "bot",
  sources?: string[],
  citations?: { text: string; page: number; file: string }[],
  onCitationClick?: (page: number, file: string) => void
}) => {
  const collapsible = useCollapsible()
  let typedText = ""
  if (message.includes("Search results found:") || message.includes("Query")) {
    typedText = useTypewriter(message, 20);
  }
  else {
    typedText = message;
  }
  const text = sender === "bot" ? typedText : message;

  return (
    <>
      {queries_ && sender === 'bot' && <ThinkingBubble queries={queries_} />}
      {(text || sources) &&
        <Flex justify={sender === "user" ? "flex-end" : "flex-start"}>
          <Box
            bg={sender === "user" ? "#9393934b" : "#2c2c2c4b"}
            color="white"
            p={3}
            borderRadius="lg"
            alignSelf={sender === "user" ? "flex-end" : "flex-start"}
            maxW="70%"
          >
            {sources &&
              <Button
                size="sm"
                variant="subtle"
                onClick={() => collapsible.setOpen(!collapsible.open)}>
                <Text fontWeight="bold">Sources: ({sources.length}) </Text>
                <Icon>
                  {collapsible.open ? <IoIosArrowDropright /> : <IoIosArrowDropdown />}
                </Icon>
              </Button>}
            <Collapsible.RootProvider value={collapsible}>
              <Collapsible.Content>
                <Stack>
                  {sources && sender === 'bot' && <SearchResults sources={sources} />}
                </Stack>
              </Collapsible.Content>
            </Collapsible.RootProvider>

            {<Text whiteSpace="pre-line">{text}</Text>}

            {citations && citations.length > 0 && (
              <Box mt={2}>
                <Text fontSize="sm" fontWeight="bold">
                  Citations:
                </Text>
                {citations.map((c, idx) => (
                  <Link
                    key={idx}
                    color="teal.300"
                    onClick={() => onCitationClick?.(c.page, c.file)}
                    cursor="pointer"
                    display="block"
                  >
                    {c.text}
                  </Link>
                ))}
              </Box>
            )}
          </Box>
        </Flex>
      }
    </>
  );
};
export default ChatBubble;
