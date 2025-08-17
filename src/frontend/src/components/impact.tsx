import { useFetch } from "../hook/useFetch"
import type { ImpactProbType } from "../types/model"
import { cn } from "../uitl"
import Loading from "./Loading"

const Impact = ()=>{
    const{isLoading, data} = useFetch<ImpactProbType>('impact_probabilities')
    return(
        <div className="opacity-0 z-10  group-hover:opacity-70 flex items-center gap-2  absolute bg-zinc-800 text-zinc-400  rounded-md w-full md:top-[10%] top-0 p-5 border border-zinc-700  md:left-full ">
            {
                isLoading && <Loading/>
            }
            {
                data &&<div className="">
                    <h3 className="text-xl font-semibold">Estimating Impact for oil price fluctuation </h3>
                    <div>
                        <progress className="bg-pink-300  rounded-md h-3 " value={data.prob_mean_increase} barClassName="my-progress"/>
                        <span className="text-sm font-medium">{data.prob_mean_increase*100}%</span>
                    </div>
                
                    </div>
            }
            {/* <div className={cn('bg-pink-300 h-1 rounded-md', `w-[${data?.prob_mean_increase*20}%]`)}></div> */}
        </div>
    )
}

export default Impact