export const instant = true;

interface ParamsProp {
    id?: number;
}

interface SearchProp {
    keyword?: string;
    search_opt?: string;
}

export default async function BoardPage({
    params,
    searchParams,
}: {
    params: ParamsProp;
    searchParams: SearchProp;
}) {
    const pathVars = await params;
    console.log('pathVars:', pathVars);

    const searchvars = await searchParams;
    console.log('searchVars', searchvars);
    return <></>;
}
