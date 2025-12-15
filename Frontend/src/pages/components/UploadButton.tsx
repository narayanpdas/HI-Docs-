import { IconButton } from "@chakra-ui/react";
import { FiUpload } from "react-icons/fi";

import { useAuth } from "./utils/authContext";

const UploadButton = () => {
  const { role } = useAuth();

  if (role !== "VIEWER") {
    return null;
  }

  return (
    <label>
      <input type="file" accept="application/pdf" hidden />
      <IconButton
        as="span"
        aria-label="Upload Document"
        colorScheme="blue"
        size="lg"
        borderRadius="full"
      ><FiUpload /></IconButton>
    </label>
  );
};

export default UploadButton;
