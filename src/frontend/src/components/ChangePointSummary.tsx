import { useFetch } from "../hook/useFetch";
import type { ChangePointType } from "../types/model";
import Impact from "./impact";
import Loading from "./Loading";

const ChangePointSummary = ()=>{
    const {isLoading, data} = useFetch<ChangePointType[]>('change_point_summary')
    return(
        <div className="relative my-10  p-5 text-zinc-600 w-full">
            <div className="my-5">
                <h3 className="text-3xl font-bold ">Change Point Summary</h3>
            </div>
            {
                isLoading && <Loading/>
            }
            <div className="my-3 grid grid-cols-3 gap-2 ">
                {
                    data?.map((change:ChangePointType)=>(
                        <div className="rounded-md   flex flex-col p-5  bg-zinc-200 cursor-pointer">
                            <span className="font-semibold">Change Point Detected:</span>
                            <span>Date: {new Date(change?.change_point_date).toDateString()}</span>
                            <span>HPD Start Date: {change?.hpd_start_date}</span>
                            <span>HPD End Date: {change?.hpd_end_date}</span>
                        </div>
                    ))
                }
            </div>
            <Impact/>
        </div>
    )
};

export default ChangePointSummary;