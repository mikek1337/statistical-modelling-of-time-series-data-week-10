import { useFetch } from "../hook/useFetch"
import type { ImpactProbType } from "../types/model"
import { cn } from "../uitl"
import Loading from "./Loading"

const Impact = ()=>{
    const{isLoading, data} = useFetch<ImpactProbType>('impact_probabilities')
    return(
        <div className="opacity-0 z-10  group-hover:opacity-70 transition-all ease-in-out duration-150 flex items-center gap-2  absolute bg-zinc-300   rounded-md w-full md:top-[10%] top-0 p-5 text-zinc-800   group-hover:md:left-full ">
            {
                isLoading && <Loading/>
            }
            {
                data &&<div className="w-full">
                    <h3 className="text-2xl font-semibold capitalize mb-4">Estimating Impact  </h3>
                    <div className="flex gap-2 items-center justify-between w-full ">
                        <div>
                            <span>Average Impact</span>

                        </div>
                        <div className="flex items-center gap-2">
                        <progress className="bg-pink-300  rounded-md h-3 " value={data.prob_mean_increase} barClassName="my-progress"/>
                        <span className="text-sm font-medium">{data.prob_mean_increase*100}%</span>
                        </div>
                    </div>
                
                    </div>
            }
            {/* <div className={cn('bg-pink-300 h-1 rounded-md', `w-[${data?.prob_mean_increase*20}%]`)}></div> */}
        </div>
    )
}

export default Impact