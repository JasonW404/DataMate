import { Boxes } from "lucide-react";
import { OperatorI } from "./operator.model";

export const mapOperator = (op: OperatorI) => {
  return {
    ...op,
    icon: <Boxes />,
  };
};
