import {
    Badge,
    Box,
    Text,
    VStack,
    HStack,
    Icon,
} from "@chakra-ui/react";
import { CiSearch } from "react-icons/ci";
const ThinkingBubble = ({ queries }: { queries: string[] }) => {
    return (

        <Box
            bg="gray.900"
            p={4}
            borderRadius="lg"
            maxW="lg"
            w="100%"
            shadow="md"
        >
            <Text
                fontWeight="bold"
                color="gray.200"
                fontSize="sm"
                mb={3}
            >
                Searched for:
            </Text>
            <VStack alignItems="flex-start">
                {queries.map((query, idx) => (
                    <HStack key={idx} >
                        <Icon as={CiSearch} color="teal.300" boxSize={4.5} flexShrink={0} />
                        <Badge
                            colorPalette="teal.800"
                            variant="subtle"
                            borderRadius="md"
                            px={2.5}
                            py={1}
                            fontSize="sm"
                            textTransform="none"
                            whiteSpace="normal"
                            wordBreak="break-word"
                            color="#b1cde8ff"
                        >
                            {query}
                        </Badge>
                    </HStack>
                ))}
            </VStack>
        </Box>
    );
};

export default ThinkingBubble;

