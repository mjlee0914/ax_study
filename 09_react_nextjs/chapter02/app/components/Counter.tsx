export const counterVar = { test1: 100, test2: 200 };

export const counterVar2 = 200;

export interface Product {
    id: number;
    main: string;
}

export default function Counter(): React.JSX.Element {
    return <div>Counter!</div>; //<div>는 태그가 아닌 jsx 객체
}
