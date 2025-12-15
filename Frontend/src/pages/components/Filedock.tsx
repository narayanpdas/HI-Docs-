import { useState } from "react";
import {
  Button, CloseButton, Drawer, Text,
  Portal, Box, AbsoluteCenter, Icon,
  CardRoot, CardHeader, CheckboxRoot,
  CheckboxHiddenInput, CheckboxControl,
  Skeleton, FileUpload,
  Flex, HStack, Spinner
} from '@chakra-ui/react'
import { IoIosMenu } from "react-icons/io";
import { HiUpload } from "react-icons/hi"
import { IoIosRefresh } from "react-icons/io";
import { Progress } from "@chakra-ui/react";
import { useAuth } from "./utils/authContext";
import { checkStatus } from "../services/authService"
import { RiDeleteBinLine, RiDeleteBinFill, } from "react-icons/ri";
import { fileUpload } from "../services/authService";
import type { FileUploadFileChangeDetails } from "@chakra-ui/react";
interface FiledockProps {
  docs: any[] | false;
  loading: boolean;
  checkedDocs: { [key: string]: boolean };
  onCheckChange: (id: string | number) => void;
  onRefresh: () => void;
  onSelectAll: () => void;
  onClearAll: () => void;
}
function delay(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
};
const Filedock = ({
  docs,
  loading,
  checkedDocs,
  onCheckChange,
  onRefresh,
  onClearAll
}: FiledockProps) => {

  const [open, setOpen] = useState(false)
  const [isUploading, setisUploading] = useState(false);
  const [uploadingProgress, setisUploadingProgress] = useState(0);
  const [uploaderkey, setUploaderKey] = useState(0)
  const [fileStatus, setFileStatus] = useState(true);
  const [fileName, setfileName] = useState('')
  const { role } = useAuth();
  const onhandleFileChange = async (details: FileUploadFileChangeDetails) => {
    const file = details.acceptedFiles[0];
    if (!file) return;
    try {
      setisUploading(true);
      setisUploadingProgress(0);
      setfileName(file.name);
      await fileUpload(file, setisUploadingProgress);
      setFileStatus(false);
      await delay(1000);
      // Delay so that the File Actually gets Uploaded this is for the
      // failsafe-refresh in case some or more time is taken for databse update.
      let counter: number = 0;
      while (counter < 10) {
        const res = await checkStatus();
        await delay(4000);
        if (res && (res['message'] === null || res['message'] === 'None')) break;
        console.log(res['message']);
        counter += 1;
      }
      onRefresh();
    }
    catch (err) {
      console.log("Sir we are doomed, here is what caused it: ", err);
    }
    finally {
      setisUploading(false);
      setisUploadingProgress(0);
      setUploaderKey(prev => prev + 1);
      setfileName('');
      setFileStatus(true);
    }
  }
  return (
    <Drawer.Root key={'start'} placement={'start'} open={open}
      onOpenChange={(e) => { setOpen(e.open); }} >
      <Drawer.Trigger asChild>
        <Button variant="outline" size="md">
          <IoIosMenu />
        </Button>
      </Drawer.Trigger >
      <Portal >
        <Drawer.Backdrop />
        <Drawer.Positioner >
          <Drawer.Content colorPalette={'cyan'}>
            <Drawer.Header>
              <Drawer.Title>Documents</Drawer.Title>
            </Drawer.Header>
            <Drawer.Body marginBottom={'0'} gap={'1'}>
              {isUploading &&
                <Progress.Root
                  value={uploadingProgress}
                  maxW="sm"
                  colorPalette={'cyan'}
                  variant={'subtle'}
                >
                  <HStack>
                    <Progress.Label maxW="80px" overflow={'clip'}>{fileName}</Progress.Label>
                    <Progress.Track flex="1">
                      <Progress.Range />
                    </Progress.Track>
                    <Progress.ValueText>{uploadingProgress}%</Progress.ValueText>
                  </HStack>
                </Progress.Root>
              }
              {loading &&
                <AbsoluteCenter gap={"3.5"} flexDirection={"column"}>
                  <Flex flexDirection={"column"} flex={"1"} gap={"1"}>
                    <Skeleton height="5" width="33%"></Skeleton>
                    <Skeleton height="5" width="66%"></Skeleton>
                    <Skeleton height="5" width="90%"></Skeleton>
                    Fetching Documents...
                  </Flex>
                </AbsoluteCenter>}
              {docs != false ?
                docs.map((doc: any) => (
                  <CardRoot display={'flex'} key={doc.id} variant="outline" maxW="sm"
                    bg={'gray.800'} justifyContent="space-between" gap={"4"}>
                    <CardHeader display="flex" flex={'2'} flexDirection={"row"}
                      alignItems="flex-start" justifyContent="space-between"
                      gap={"2"}
                    ><Text wordWrap={'break-word'} whiteSpace="nowrap" overflow="hidden"
                      boxSize={'21'} textOverflow="ellipsis" marginBottom={"1rem"}>{doc.filename}</Text>
                      <Box display={'flex'} alignItems={'center'} justifySelf={"center"} gap={'3'} >
                        {role == "ADMIN" &&
                          <Button _hover={{ bg: 'gray.500' }} aria-label="Send"
                            colorScheme="blue" className="group" size={'xs'} bg={'gray.600'}>
                            <Icon as={RiDeleteBinLine} opacity={1} _groupHover={{ opacity: 0 }}
                              transition="opacity 0.2s" />
                            <Icon as={RiDeleteBinFill} opacity={0} _groupHover={{ opacity: 1, color: 'red.700' }}
                              transition="opacity 0.2s" position="absolute" /></Button>
                        }
                        {!fileStatus && <Spinner />}
                        {fileStatus &&
                          <CheckboxRoot
                            onCheckedChange={() => {
                              onCheckChange(doc.id);
                            }}
                            checked={checkedDocs[doc.id]}
                            defaultChecked
                            size={'md'} variant={'subtle'} colorPalette={'teal'}>
                            <CheckboxHiddenInput />
                            <CheckboxControl />
                          </CheckboxRoot>
                        }
                      </Box>
                    </CardHeader>
                  </CardRoot>
                ))
                : true}
              {(loading == false && docs == false) ? <Box>Error Loading Docs</Box> : false}
            </Drawer.Body>
            <Drawer.Footer justifyContent={"center"}>
              <FileUpload.Root
                key={uploaderkey}
                accept={["application/pdf"]}
                maxFiles={1}
                onFileChange={onhandleFileChange}
              >
                <FileUpload.HiddenInput />
                <FileUpload.Trigger asChild>
                  <Button variant={'outline'} >
                    <HiUpload />Upload
                  </Button>
                </FileUpload.Trigger>
              </FileUpload.Root>
              <Button variant="outline" onClick={() => { onRefresh(); }}>
                <IoIosRefresh />
              </Button>
              <Button variant="outline" onClick={() => {
                onClearAll();
                console.log("all items cleared.")
              }}>Clear All</Button>
            </Drawer.Footer>
            <Drawer.CloseTrigger asChild>
              <CloseButton size="sm" />
            </Drawer.CloseTrigger>
          </Drawer.Content>
        </Drawer.Positioner>
      </Portal >
    </Drawer.Root >
  );
};

export default Filedock;