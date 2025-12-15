import  {IconButton,Link} from "@chakra-ui/react" 
// import {Tooltip}  from "@chakra-ui/react/tooltip";
import { ImNewTab } from "react-icons/im";

const Openinnewwindow = ({ pdfUrl, page }: { pdfUrl: string,page:number }) => {
    const finalUrl = page ? `${pdfUrl}#page=${page}` : pdfUrl;
    return (
    <Link href={finalUrl} as="a" target="_blank" alignSelf={"flex-start"}>
        <ImNewTab size={24}/>
      </Link>
  );
};
export default Openinnewwindow;