import { useState, type FC } from "react"


type DarkModeType = {
    children:React.ReactNode
}

const DarkMode:FC<DarkModeType> = ({children})=>{
    const[darkMode, isDarkMode] = useState(false);

}