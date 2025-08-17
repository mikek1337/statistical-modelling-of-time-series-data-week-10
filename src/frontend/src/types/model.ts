export type ChangePointType = {
    change_point_date:string,
    hpd_start_date:string,
    hpd_end_date:string,
    tau_post_index: number
}

export type ImpactProbType={
    prob_mean_increase: number,
    prob_sd_increase: number
}