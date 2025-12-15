import { Button, Menu, Portal } from "@chakra-ui/react"
import { useState } from "react"
import { MdManageSearch } from "react-icons/md";
import { IoIosLock } from "react-icons/io";
import { getKey } from "@/pages/services/authService";
import { useEffect } from "react";
const SearchSpace = ({ onTopNChange, keyingest }:
    { onTopNChange: (top_n: number) => void, keyingest: string }) => {
    const [value, setValue] = useState("Precise")
    const [apikey, setKey] = useState<string>()
    const items = [
        { title: "Precise", value: "Precise", id: 0 },
        { title: "Broad-Search", value: "Balanced", id: 1 },
        { title: "Comprehensive", value: "Comprehensive", id: 2 },
    ]
    const handletopn = (e: { value: string }) => {
        const newValue = e.value;
        setValue(newValue)
        const selectedItem = items.find(item => item.title === newValue);
        if (selectedItem) onTopNChange(selectedItem.id);
    }
    useEffect(() => {
        const fetchkey = async () => {
            const apikey = await getKey();
            console.log(apikey)
            if (apikey) { setKey(apikey) }
        }
        fetchkey();
    }, [keyingest])
    return (
        <Menu.Root>
            <Menu.Trigger asChild >
                <Button variant="outline" size="md" bg={'gray.800'}>
                    <MdManageSearch color="cyan" />
                </Button>
            </Menu.Trigger>
            <Portal>
                <Menu.Positioner>
                    <Menu.Content minW="10rem">
                        <Menu.RadioItemGroup
                            value={value}
                            onValueChange={(e) => handletopn(e)} >
                            {items.map((item) => (
                                <Menu.RadioItem key={item.value} value={item.value} disabled={apikey === undefined} >
                                    {apikey === undefined && item.title != "Precise" && <IoIosLock color="gold" size={'20'} />}{item.title}
                                    <Menu.ItemIndicator />
                                </Menu.RadioItem>
                            ))}
                        </Menu.RadioItemGroup>
                    </Menu.Content>
                </Menu.Positioner>
            </Portal>
        </Menu.Root>
    )
};
export default SearchSpace;