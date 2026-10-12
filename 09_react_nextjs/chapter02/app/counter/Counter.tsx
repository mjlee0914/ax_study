'use client'; // CSR

import { useState } from 'react';

export default function Counter(): React.JSX.Element {
    const [number, setNumber] = useState<number>(0);

    // function incNum() {
    //     setNumber(number + 1);
    // }

    // function decNum() {
    //     setNumber(number - 1);
    // }

    const incNum = () => setNumber(number + 1);

    const decNum = () => setNumber(number - 1);

    return (
        <>
            <button
                onClick={decNum}
                type="button"
                className="border m-2 hover:bg-zinc-700 cursor-pointer"
            >
                -1
            </button>
            <h1 className="flex justify-center text-2xl">count: {number}</h1>
            <button
                onClick={incNum}
                type="button"
                className="border m-2 hover:bg-zinc-700 cursor-pointer"
            >
                +1
            </button>
        </>
    );
}
