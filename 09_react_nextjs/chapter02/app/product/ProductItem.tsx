import Badge from '../components/Badge';

interface Product {
    itemName: string;
    itemPrice: number;
}

export default function ProductItem({
    itemName,
    itemPrice,
}: Product): React.JSX.Element {
    return (
        <>
            <dl>
                <dt>상품명</dt>
                <dd>
                    <Badge theme="dark">{children}</Badge>
                    <br />
                    {itemName}
                </dd>
            </dl>
            <dl>
                <dt>판매가</dt>
                <dd>{itemPrice}</dd>
            </dl>
            <dl>
                <dt>할인 여부</dt>
            </dl>
        </>
    );
}
