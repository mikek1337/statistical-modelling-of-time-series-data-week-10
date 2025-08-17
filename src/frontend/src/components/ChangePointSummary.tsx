import { useFetch } from "../hook/useFetch";
import type { ChangePointType } from "../types/model";
import Impact from "./impact";
import Loading from "./Loading";

const ChangePointSummary = ()=>{
    const {isLoading, data} = useFetch<ChangePointType>('change_point_summary')
    return(
        <div className="relative my-10  p-5 text-zinc-600 md:w-3/4 group">
            <div className="my-5">
                <h3 className="text-3xl font-bold ">Change Point Summary</h3>
            </div>
            {
                isLoading && <Loading/>
            }
            <div className="rounded-md   flex flex-col p-5  bg-zinc-400 cursor-pointer">
                <span className="font-semibold">Change Point Detected:</span>
                <span>Date: {new Date(data?.change_point_date).toDateString()}</span>
                <span>HPD Start Date: {data?.hpd_start_date}</span>
                <span>HPD End Date: {data?.hpd_end_date}</span>
            </div>
            <Impact/>
        </div>
    )
};

export default ChangePointSummary;