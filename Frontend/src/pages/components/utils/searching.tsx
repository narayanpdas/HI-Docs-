import { Flex, Text, Box, Skeleton } from "@chakra-ui/react";

const SearchingIndicator = () => {
  return (
    <>
      <Flex
        align="center"
        gap="2"
        p="4"
        bg="gray.700"
        borderRadius="lg"
        maxW="fit-content"
      >
        <Flex gap="1" align="center">
          <Box
            w="2"
            h="2"
            bg="blue.400"
            borderRadius="full"
            animation="bounce 1.4s ease-in-out infinite"
          />
          <Box
            w="2"
            h="2"
            bg="blue.400"
            borderRadius="full"
            animation="bounce 1.4s ease-in-out 0.2s infinite"
          />
          <Box
            w="2"
            h="2"
            bg="blue.400"
            borderRadius="full"
            animation="bounce 1.4s ease-in-out 0.4s infinite"
          />
        </Flex>

        {/* Searching text with pulse */}
        <Text
          fontSize="sm"
          color="gray.300"
          animation="pulse 2s ease-in-out infinite"
        >
          Connecting...
        </Text>

      </Flex>
      <Skeleton height="5" width="70%"></Skeleton>
      <Skeleton height="5" width="55%"></Skeleton>
      <Skeleton height="5" width="35%"></Skeleton>

    </>
  );
};

export default SearchingIndicator;