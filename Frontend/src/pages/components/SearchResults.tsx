import { Text, Link } from "@chakra-ui/react";
import { HiDocumentSearch } from "react-icons/hi";

const SearchResults = ({ sources }: { sources: string[] }) => {
    // console.log(sources, "From SR")
    return (
        <>
            <div style={{ "marginTop": "0.5rem" }}>
                {sources.map((source, idx) => (
                    <div key={idx}>
                        <Link colorPalette="teal">{source}<HiDocumentSearch /></Link>
                    </div>
                ))}
            </div>
        </>
    )
};
export default SearchResults;