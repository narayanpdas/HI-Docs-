import {
    Box, Text, Dialog, CloseButton, Portal, Button, Input
} from "@chakra-ui/react";
import { FaRegSave } from "react-icons/fa";
// import { useForm } from "react-hook-form";
import { useState } from "react";


const ApiPopup = ({ setapi }: { setapi: (value: string) => void }) => {
    const [Apikey, setApikey] = useState("");

    const handleInputChange = (event: any) => {
        setApikey(event.target.value)
    }
    const saveApi = () => {
        sessionStorage.setItem("apikey", Apikey);
        setapi(Apikey);
    }
    return (
        <Dialog.Root>
            <Dialog.Trigger asChild>
                <Button variant="outline" size={'lg'}>API Key</Button>
            </Dialog.Trigger>
            <Portal>
                <Dialog.Backdrop />
                <Dialog.Positioner>
                    <Dialog.Content>
                        <Dialog.CloseTrigger asChild>
                            <CloseButton />
                        </Dialog.CloseTrigger>
                        <Dialog.Header>
                            <Dialog.Title></Dialog.Title>
                        </Dialog.Header>
                        <Dialog.Body>
                            <Box gap={'2'} display={'flex'} flexDirection={'column'}>
                                <Box gap={'2'} display={'flex'} flexDirection={'row'}>
                                    <Input
                                        value={Apikey}
                                        placeholder="Enter your Gemini API Key Here..."
                                        onChange={handleInputChange}
                                    />
                                    <Button variant="outline"
                                        onClick={saveApi}>
                                        <FaRegSave />
                                    </Button>
                                </Box>
                                <Text>This Key is stored in sessionStorage and will be deleted once this session is exited.</Text>

                            </Box>
                        </Dialog.Body>
                        <Dialog.Footer />
                    </Dialog.Content>
                </Dialog.Positioner>
            </Portal>
        </Dialog.Root>
    )
}
export default ApiPopup;





