import { useEffect, useMemo, useState } from "react";

type useFetchReturn<T> = {
    isLoading:boolean,
    data:T,
}
export function useFetch<T>(endPoint:string){
    const[isLoading, setIsLoading] = useState(false);
    const[data, setData] = useState<T>();
     useMemo(()=>{
        fetch(`${import.meta.env.VITE_BACKEND_API_URL}/${endPoint}`).then((res)=>{
            setIsLoading(true);
            return res.json();
        }).then((res:T)=>{
           setData(res)
           
        }).catch((err)=>{
            console.log(err)
        }).finally(()=>{
            setIsLoading(false);
        });
    },[endPoint])
    // useEffect(()=>{
        
    // },[])  
    
        return {
            isLoading,
            data
        } as useFetchReturn<T>
}
