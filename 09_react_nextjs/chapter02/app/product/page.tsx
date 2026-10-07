// import { Fragment } from 'react';

// export default function ProductPage(): React.JSX.Element {
//     const itemName = '아이폰 18';
//     const itemPrice = 10000;
//     const isSoldOut = true;

//     const styles = {
//         backgroundColor: 'skyblue',
//         height: '1rem',
//     };

//     return (
//         <>
//             <dl>
//                 <dt style={{ backgroundColor: 'pink', color: 'black' }}>
//                     상품명
//                 </dt>
//                 <dd>{itemName}</dd>
//             </dl>
//             {/* isSoldOut ? <div>품절~</div> : '' */}
//             {isSoldOut && <div>품절</div>}
//             <dl style={styles}>
//                 <dt>판매가</dt>
//                 <dd>{itemPrice}</dd>
//             </dl>
//         </>
//     );
// }

import ProductItem from './ProductItem';

export default function ProductPage(): React.JSX.Element {
    return <ProductItem item-name="아이폰" item-price={10000} />;
}
